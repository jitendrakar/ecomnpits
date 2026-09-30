import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import ProductCategory

data = {
    'cctv-security': {
        'title': 'CCTV Camera Selection & HD DVR Setup Guide',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Learn how to choose between 2MP, 5MP, and 4K IP cameras, DVR/NVR storage calculations, and night-vision capabilities for office and home security.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Feature / Spec</th>
                        <th>2MP HD Dome/Bullet</th>
                        <th>5MP Smart IP Camera</th>
                        <th>4K 8MP PTZ Outdoor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Resolution</strong></td><td>1080p Full HD</td><td>2K (2560x1920)</td><td>4K Ultra HD (3840x2160)</td></tr>
                    <tr><td><strong>Night Vision</strong></td><td>20 Meters IR</td><td>30M Color Night Vision</td><td>50M Smart IR + Floodlight</td></tr>
                    <tr><td><strong>Storage Need / Day</strong></td><td>~20 GB per Cam</td><td>~35 GB per Cam</td><td>~60 GB per Cam (H.265+)</td></tr>
                    <tr><td><strong>Ideal Use Case</strong></td><td>Indoor Office & Retail</td><td>Building Entrances & Perimeters</td><td>Large Warehouses & Highways</td></tr>
                    <tr><td><strong>Best Advantage</strong></td><td>Cost Effective & Simple</td><td>High Clarity & Face Detail</td><td>360 Pan-Tilt-Zoom & AI Auto-Track</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'computer-components': {
        'title': 'PC Hardware Buyer Guide: CPU, RAM & Motherboard Compatibility',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Step-by-step walkthrough on pairing Intel/AMD processors with compatible motherboard chipsets, DDR4 vs DDR5 RAM, and GPU power requirements.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Component Category</th>
                        <th>Entry-Level / Office</th>
                        <th>Mid-Range / Gaming</th>
                        <th>Enterprise / Workstation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Processor (CPU)</strong></td><td>Intel Core i3 / Ryzen 3</td><td>Intel Core i5 / Ryzen 5</td><td>Intel Core i7/i9 / Ryzen 7/9</td></tr>
                    <tr><td><strong>Memory (RAM)</strong></td><td>8GB DDR4 (3200MHz)</td><td>16GB - 32GB DDR4/DDR5</td><td>64GB+ DDR5 ECC Memory</td></tr>
                    <tr><td><strong>Graphics (GPU)</strong></td><td>Integrated HD Graphics</td><td>NVIDIA RTX 4060 / RX 7600</td><td>NVIDIA RTX 4080 / Quadro AI</td></tr>
                    <tr><td><strong>Power Supply (PSU)</strong></td><td>450W 80+ Bronze</td><td>650W 80+ Gold Semi-Modular</td><td>850W - 1000W 80+ Gold Fully Modular</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'desktop-computers': {
        'title': 'Office Desktop vs Custom Workstation PC Comparison',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Detailed video guide on choosing pre-built brand desktops vs custom-assembled workstation PCs for AutoCAD, video editing, and daily office tasks.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Desktop Type</th>
                        <th>Commercial Office PC</th>
                        <th>Editing Workstation</th>
                        <th>Gaming & AI Workstation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Primary Usage</strong></td><td>Tally, MS Office, Browsing</td><td>Video Editing, 3D Rendering</td><td>AAA Gaming, Machine Learning</td></tr>
                    <tr><td><strong>Processor Tier</strong></td><td>Intel Core i3/i5 12th Gen</td><td>Intel Core i7/i9 14th Gen</td><td>AMD Ryzen 9 7900X / i9 14900K</td></tr>
                    <tr><td><strong>Storage Combo</strong></td><td>512GB NVMe M.2 SSD</td><td>1TB NVMe + 2TB HDD</td><td>2TB Gen4 NVMe SSD</td></tr>
                    <tr><td><strong>Warranty & Support</strong></td><td>3 Years Brand On-Site</td><td>3 Years Nehru Place Hub SLA</td><td>Component-by-Component Warranty</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'laptops-notebooks': {
        'title': 'Commercial Laptop Buying Guide: Business vs Ultrabook vs Gaming',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Discover battery efficiency, display panel types (IPS vs OLED), military-grade durability standards, and expansion options across laptops.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Laptop Category</th>
                        <th>Business Notebook</th>
                        <th>Thin & Light Ultrabook</th>
                        <th>High-Performance Gaming</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Target Audience</strong></td><td>Executives & Corporate Teams</td><td>Travelers & Students</td><td>Gamers, Designers, Architects</td></tr>
                    <tr><td><strong>Battery Life</strong></td><td>8 - 10 Hours</td><td>10 - 14 Hours</td><td>3 - 5 Hours</td></tr>
                    <tr><td><strong>Weight & Build</strong></td><td>1.6 kg (Durable Chassis)</td><td>1.1 kg (Magnesium-Alloy)</td><td>2.3 kg (High Thermal Vents)</td></tr>
                    <tr><td><strong>Port Selection</strong></td><td>HDMI, Type-C, RJ45, USB-A</td><td>Thunderbolt 4 / Type-C</td><td>HDMI 2.1, Ethernet, Thunderbolt</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'networking-hardware': {
        'title': 'Enterprise Networking Setup: Routers, Switches & Fiber Patching',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Learn how to plan high-speed office networking, PoE switch calculations for IP cameras, rack management, and Cat6 gigabit throughput.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Equipment Type</th>
                        <th>Unmanaged Switch</th>
                        <th>PoE+ Managed Switch</th>
                        <th>Wi-Fi 6 Enterprise AP</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Application</strong></td><td>Plug & Play Desktop Network</td><td>CCTV Camera Power & Data</td><td>High-Density Wireless Office</td></tr>
                    <tr><td><strong>Bandwidth Speed</strong></td><td>10/100/1000 Mbps Gigabit</td><td>1 Gigabit + 10G SFP+ Uplink</td><td>AX3000 Wi-Fi 6 (3.0 Gbps)</td></tr>
                    <tr><td><strong>Power Delivery</strong></td><td>Standard AC Power</td><td>PoE / PoE+ (30W per port)</td><td>Power over Ethernet (802.3at)</td></tr>
                    <tr><td><strong>VLAN & Security</strong></td><td>Basic Forwarding</td><td>L2/L3 Management, VLANs</td><td>WPA3 Enterprise, Guest Portal</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'storage-hard-drives': {
        'title': 'HDD vs SATA SSD vs NVMe M.2 SSD Performance & Lifespan Guide',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Understanding Read/Write speeds, TBW endurance ratings, surveillance 24/7 hard drives (Seagate SkyHawk / WD Purple), and NVMe Gen4 speeds.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Storage Spec</th>
                        <th>Surveillance HDD (3.5 inch)</th>
                        <th>SATA III 2.5 inch SSD</th>
                        <th>NVMe M.2 PCIe Gen4 SSD</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Sequential Read Speed</strong></td><td>180 MB/s</td><td>550 MB/s</td><td>7,000+ MB/s</td></tr>
                    <tr><td><strong>Duty Cycle</strong></td><td>24x7 Continuous Write</td><td>Standard Workload</td><td>High-Performance Workload</td></tr>
                    <tr><td><strong>Best Suited For</strong></td><td>DVR/NVR CCTV Recording</td><td>Legacy Laptop/PC Upgrades</td><td>OS Drive, Gaming & 4K Editing</td></tr>
                    <tr><td><strong>Durability & Noise</strong></td><td>Mechanical (Low Vibration)</td><td>Solid State (Silent, Zero Shock)</td><td>Solid State (Ultra-Fast)</td></tr>
                </tbody>
            </table>
        </div>
        '''
    }
}

for slug, info in data.items():
    cat = ProductCategory.objects.filter(slug=slug).first()
    if cat:
        cat.learning_video_title = info['title']
        cat.learning_video_url = info['url']
        cat.learning_video_description = info['desc']
        cat.comparison_guide_html = info['guide']
        cat.save()
        print(f'Successfully updated Category: {cat.name}')
    else:
        print(f'Category with slug {slug} not found')
