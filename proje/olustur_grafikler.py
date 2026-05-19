import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import carwash_sim
import numpy as np

# Modern Dashboard Renk Paleti
COLORS = {'small': '#38bdf8', 'large': '#f59e0b', 'service': '#ef4444', 'total': '#10b981'}

def generate_wait_time_graph():
    # Küçük kabin sayısına göre analiz (Diğer kaynaklar sabit)
    small_bays_list = [1, 2, 4, 6, 8]
    small_waits = []
    large_waits = []
    service_waits = []
    
    for b in small_bays_list:
        res = carwash_sim.run_carwash_sim(
            small_bays=b, 
            large_bays=2, 
            service_bays=1,
            small_wash_staff=3, small_dry_staff=2,
            large_wash_staff=2, large_dry_staff=1,
            service_wash_staff=1, service_dry_staff=1,
            arrival_rate=5.0, 
            sim_time=480
        )
        small_waits.append(res['metrics']['small']['wash'])
        large_waits.append(res['metrics']['large']['wash'])
        service_waits.append(res['metrics']['service']['wash'])
        
    plt.figure(figsize=(10, 6), facecolor='#0f172a')
    ax = plt.axes()
    ax.set_facecolor('#1e293b')
    
    plt.plot(small_bays_list, small_waits, marker='o', color=COLORS['small'], label='Küçük Araç Yıkama Bekleme', linewidth=3)
    plt.plot(small_bays_list, large_waits, marker='s', color=COLORS['large'], label='Büyük Araç Yıkama Bekleme', linewidth=3)
    plt.plot(small_bays_list, service_waits, marker='^', color=COLORS['service'], label='Görevli Araç Yıkama Bekleme', linewidth=3)
    
    plt.title('Araç Tiplerine Göre Yıkama Bekleme Süreleri', fontsize=16, color='white', fontweight='bold')
    plt.xlabel('Küçük Kabin Sayısı (Değişken)', fontsize=12, color='#94a3b8')
    plt.ylabel('Ortalama Bekleme Süresi (Dakika)', fontsize=12, color='#94a3b8')
    plt.xticks(small_bays_list, color='white')
    plt.yticks(color='white')
    
    legend = plt.legend(facecolor='#1e293b', edgecolor='#334155')
    for text in legend.get_texts(): text.set_color('white')
    
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.savefig('grafik_bekleme_sureleri.png', dpi=300)
    plt.close()

def generate_capacity_graph():
    arrival_rates = [2.0, 5.0, 10.0, 15.0]
    total_washed = []
    
    for a in arrival_rates:
        res = carwash_sim.run_carwash_sim(
            small_bays=2, large_bays=1, service_bays=1,
            small_wash_staff=2, small_dry_staff=2,
            large_wash_staff=1, large_dry_staff=1,
            service_wash_staff=1, service_dry_staff=1,
            arrival_rate=a, 
            sim_time=480
        )
        total_washed.append(res['metrics']['total_completed'])

    plt.figure(figsize=(10, 6), facecolor='#0f172a')
    ax = plt.axes()
    ax.set_facecolor('#1e293b')
    
    bars = plt.bar([str(int(a))+" Dk" if a.is_integer() else str(a)+" Dk" for a in arrival_rates], total_washed, color=COLORS['total'])
    plt.title('Geliş Sıklığına Göre Tamamlanan Toplam Araç Sayısı', fontsize=16, color='white', fontweight='bold')
    plt.xlabel('Araç Geliş Sıklığı (Ortalama Dakika)', fontsize=12, color='#94a3b8')
    plt.ylabel('Toplam Tamamlanan Araç', fontsize=12, color='#94a3b8')
    
    plt.xticks(color='white')
    plt.yticks(color='white')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')
                 
    plt.grid(axis='y', linestyle='--', alpha=0.1)
    plt.tight_layout()
    plt.savefig('grafik_kapasite_analizi.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Simülasyon koşturuluyor ve grafikler üretiliyor...")
    generate_wait_time_graph()
    generate_capacity_graph()
    print("Grafikler başarıyla oluşturuldu: grafik_bekleme_sureleri.png, grafik_kapasite_analizi.png")
