import simpy
import random
import json

# Araç Tipleri ve Özellikleri
VEHICLE_CONFIG = {
    "Motor": {
        "prob": 0.15,
        "wash_time": (3, 5),
        "dry_time": (5, 8),
        "bay_type": "small_bays",
        "wash_staff": "small_wash_staff",
        "dry_staff": "small_dry_staff"
    },
    "Otomobil": {
        "prob": 0.50,
        "wash_time": (5, 8),
        "dry_time": (10, 15),
        "bay_type": "small_bays",
        "wash_staff": "small_wash_staff",
        "dry_staff": "small_dry_staff"
    },
    "Otobüs": {
        "prob": 0.15,
        "wash_time": (15, 20),
        "dry_time": (20, 30),
        "bay_type": "large_bays",
        "wash_staff": "large_wash_staff",
        "dry_staff": "large_dry_staff"
    },
    "Tır": {
        "prob": 0.10,
        "wash_time": (20, 30),
        "dry_time": (30, 45),
        "bay_type": "large_bays",
        "wash_staff": "large_wash_staff",
        "dry_staff": "large_dry_staff"
    },
    "Görevli Araç": {
        "prob": 0.10,
        "wash_time": (8, 12),
        "dry_time": (15, 20),
        "bay_type": "service_bays",
        "wash_staff": "service_wash_staff",
        "dry_staff": "service_dry_staff"
    }
}

def car(env, name, carwash, stats, events):
    """Bir aracın sürecini simüle eder."""
    arrival_time = env.now
    
    # Araç tipini belirle
    r = random.random()
    cumulative_prob = 0
    v_type_name = "Otomobil"
    for t_name, cfg in VEHICLE_CONFIG.items():
        cumulative_prob += cfg['prob']
        if r <= cumulative_prob:
            v_type_name = t_name
            break
            
    config = VEHICLE_CONFIG[v_type_name]
    
    events.append({
        "time": arrival_time, "car": name, "v_type": v_type_name,
        "type": "arrival", "msg": f"{name} ({v_type_name}) istasyona ulaştı."
    })

    # 1. YIKAMA AŞAMASI (Kabin + Yıkama Personeli gerekiyor)
    bay_res = carwash[config['bay_type']]
    wash_staff_res = carwash[config['wash_staff']]
    
    # Kategori belirle (İstatistik için)
    category = 'small'
    if config['bay_type'] == 'large_bays': category = 'large'
    elif config['bay_type'] == 'service_bays': category = 'service'

    with bay_res.request() as bay_req, wash_staff_res.request() as staff_req:
        yield simpy.AllOf(env, [bay_req, staff_req])
        
        wait_for_wash = env.now - arrival_time
        stats[category]['wash'].append(wait_for_wash)
        
        events.append({
            "time": env.now, "car": name, "v_type": v_type_name, "type": "enter_wash", 
            "msg": f"{name} yıkamaya alındı. (Kabin ve Yıkama Personeli hazır)"
        })
        
        yield env.timeout(random.uniform(*config['wash_time']))
        events.append({
            "time": env.now, "car": name, "v_type": v_type_name, "type": "finish_wash", 
            "msg": f"{name} yıkandı, kurulama bekliyor."
        })

    # 2. KURULAMA AŞAMASI (Sadece Kurulama Personeli gerekiyor - Kabinden çıktı)
    ready_for_dry_time = env.now
    dry_staff_res = carwash[config['dry_staff']]
    
    with dry_staff_res.request() as request:
        yield request
        wait_for_dry = env.now - ready_for_dry_time
        stats[category]['dry'].append(wait_for_dry)
        
        events.append({
            "time": env.now, "car": name, "v_type": v_type_name, "type": "enter_dry", 
            "msg": f"{name} kurulama personeline teslim edildi."
        })
        
        yield env.timeout(random.uniform(*config['dry_time']))
        events.append({
            "time": env.now, "car": name, "v_type": v_type_name, "type": "finish_dry", 
            "msg": f"{name} tertemiz ayrıldı."
        })
        
        stats['total_completed'] += 1
        stats['type_counts'][v_type_name] = stats['type_counts'].get(v_type_name, 0) + 1

def setup(env, params, stats, events):
    carwash = {
        'small_bays': simpy.Resource(env, int(params['small_bays'])),
        'large_bays': simpy.Resource(env, int(params['large_bays'])),
        'service_bays': simpy.Resource(env, int(params['service_bays'])),
        'small_wash_staff': simpy.Resource(env, int(params['small_wash_staff'])),
        'small_dry_staff': simpy.Resource(env, int(params['small_dry_staff'])),
        'large_wash_staff': simpy.Resource(env, int(params['large_wash_staff'])),
        'large_dry_staff': simpy.Resource(env, int(params['large_dry_staff'])),
        'service_wash_staff': simpy.Resource(env, int(params['service_wash_staff'])),
        'service_dry_staff': simpy.Resource(env, int(params['service_dry_staff']))
    }
    
    i = 0
    arrival_rate = params.get('arrival_rate', 10.0)
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_rate))
        i += 1
        env.process(car(env, f"Araç #{i}", carwash, stats, events))

def run_carwash_sim(small_bays=2, large_bays=1, service_bays=1,
                    small_wash_staff=2, small_dry_staff=2, 
                    large_wash_staff=1, large_dry_staff=1,
                    service_wash_staff=1, service_dry_staff=1, 
                    arrival_rate=10.0, sim_time=480):
    random.seed(42)
    env = simpy.Environment()
    
    params = {
        "small_bays": small_bays, "large_bays": large_bays, "service_bays": service_bays,
        "small_wash_staff": small_wash_staff, "small_dry_staff": small_dry_staff,
        "large_wash_staff": large_wash_staff, "large_dry_staff": large_dry_staff,
        "service_wash_staff": service_wash_staff, "service_dry_staff": service_dry_staff,
        "arrival_rate": arrival_rate, "sim_time": sim_time
    }
    
    # İstatistikleri Kategorize Et
    stats = {
        'small': {'wash': [], 'dry': []},
        'large': {'wash': [], 'dry': []},
        'service': {'wash': [], 'dry': []},
        'total_completed': 0,
        'type_counts': {}
    }
    events = []
    
    env.process(setup(env, params, stats, events))
    env.run(until=sim_time)
    
    def get_avg(lst):
        return round(sum(lst) / len(lst), 2) if lst else 0

    return {
        "parameters": params,
        "metrics": {
            "total_completed": stats['total_completed'],
            "small": {
                "wash": get_avg(stats['small']['wash']),
                "dry": get_avg(stats['small']['dry'])
            },
            "large": {
                "wash": get_avg(stats['large']['wash']),
                "dry": get_avg(stats['large']['dry'])
            },
            "service": {
                "wash": get_avg(stats['service']['wash']),
                "dry": get_avg(stats['service']['dry'])
            },
            "vehicle_stats": stats['type_counts']
        },
        "events": events
    }
