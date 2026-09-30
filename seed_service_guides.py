import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import ServiceCategory

data = {
    'cctv-installation': {
        'title': 'CCTV Security & Surveillance Installation SLA Walkthrough',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Step-by-step video guide explaining camera positioning, DVR/NVR network configuration, mobile app remote view setup, and AMC SLA maintenance terms.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Service Tier</th>
                        <th>Standard Home Setup</th>
                        <th>Corporate Office SLA</th>
                        <th>Industrial 24x7 Multi-Site</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Camera Count</strong></td><td>4 - 8 Cameras</td><td>8 - 16 Cameras</td><td>32+ Cameras / Multi-Location</td></tr>
                    <tr><td><strong>On-Site Response Time</strong></td><td>24 Hours</td><td>Same Day (Under 4 Hours)</td><td>2 Hour Priority Emergency SLA</td></tr>
                    <tr><td><strong>DVR/NVR Storage</strong></td><td>1TB HDD included</td><td>2TB H.265+ Surveillance HDD</td><td>RAID Storage Rack + Cloud Backup</td></tr>
                    <tr><td><strong>Warranty & AMC</strong></td><td>1 Year On-Site Warranty</td><td>1 Year AMC + Quarterly Maintenance</td><td>2 Years Full Comprehensive AMC</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'website-development': {
        'title': 'Custom Web Engineering & E-Commerce Development Guide',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Discover our software engineering process: Django/Python backend architecture, mobile-responsive UI design, automated payment gateway integration, and SEO optimization.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Web Package Level</th>
                        <th>Business Portal</th>
                        <th>E-Commerce Store</th>
                        <th>Custom Enterprise ERP / SaaS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Pages & Architecture</strong></td><td>5 - 8 Responsive Pages</td><td>Unlimited Catalog & Cart</td><td>Custom Modules & API Integrations</td></tr>
                    <tr><td><strong>Payment Gateway</strong></td><td>Inquiry Forms / WhatsApp</td><td>Automated UPI QR + IDFC IMAP</td><td>Multi-Currency Credit/Debit/Netbanking</td></tr>
                    <tr><td><strong>Delivery Time</strong></td><td>3 - 5 Business Days</td><td>7 - 10 Business Days</td><td>15 - 30 Days (Agile Sprints)</td></tr>
                    <tr><td><strong>Free Extras</strong></td><td>Free SSL + 1 Year Domain</td><td>Free SSL + Automated Email Alerts</td><td>Dedicated Cloud Server + 1 Year SLA</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'networking-services': {
        'title': 'Enterprise Office Networking, VLAN & Wi-Fi Deployment Guide',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Overview of Cat6 cabling, server rack management, PoE switch setup, router load balancing, and high-density Wi-Fi 6 access point installation.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Network Plan</th>
                        <th>Small Office (10 Users)</th>
                        <th>Corporate Office (50 Users)</th>
                        <th>Multi-Floor Enterprise (100+ Users)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Switch Equipment</strong></td><td>8-Port Unmanaged Gigabit Switch</td><td>24-Port Managed PoE+ Switch</td><td>48-Port L3 Core Switch + 10G SFP</td></tr>
                    <tr><td><strong>Wi-Fi Access Points</strong></td><td>1 Dual-Band Access Point</td><td>3 Wi-Fi 6 Mesh APs</td><td>6+ Enterprise Ceiling Mount APs</td></tr>
                    <tr><td><strong>Network Security</strong></td><td>Basic WPA2 Password</td><td>VLAN Segmentation + Firewall</td><td>Radius Enterprise Auth + Fortinet UTM</td></tr>
                    <tr><td><strong>SLA Response</strong></td><td>Next Business Day</td><td>Same Day Dispatch</td><td>2-Hour On-Site Emergency Support</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'computer-repair': {
        'title': 'Chip-Level Laptop Repair & Hardware Upgrade Demo',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Watch how certified engineers diagnose motherboard short circuits, replace cracked FHD screens, clean thermal paste, and upgrade NVMe SSDs at Nehru Place Hub.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>Repair Service</th>
                        <th>Basic Diagnostics & Upgrade</th>
                        <th>Screen / Battery Replacement</th>
                        <th>Motherboard Chip-Level Repair</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Time Duration</strong></td><td>30 Mins Express</td><td>1 Hour Same Day</td><td>24 - 48 Hours Tech Testing</td></tr>
                    <tr><td><strong>Diagnostic Fee</strong></td><td>FREE at Nehru Place Hub</td><td>FREE at Nehru Place Hub</td><td>Waived off upon repair confirmation</td></tr>
                    <tr><td><strong>Parts Used</strong></td><td>Original Brand Components</td><td>100% Genuine OEM Screens</td><td>IC Chips / MOSFET Original Replacement</td></tr>
                    <tr><td><strong>Service Warranty</strong></td><td>3 Months Warranty</td><td>6 Months Warranty</td><td>90 Days Chip-Level Warranty</td></tr>
                </tbody>
            </table>
        </div>
        '''
    },
    'it-support-amc': {
        'title': 'Corporate IT Support & AMC Contract Walkthrough',
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'desc': 'Detailed walkthrough of annual maintenance contracts (AMC), dedicated engineer placement, server backup automation, and workstation preventive maintenance.',
        'guide': '''
        <div class="table-responsive">
            <table class="table table-dark table-hover table-striped align-middle rounded-3 overflow-hidden">
                <thead class="table-primary text-dark">
                    <tr>
                        <th>AMC Tier</th>
                        <th>Basic On-Call AMC</th>
                        <th>Comprehensive Standard AMC</th>
                        <th>Enterprise Dedicated SLA</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Hardware Replacement</strong></td><td>Parts Billed Extra</td><td>All Major Components Included</td><td>100% Parts + Standby Units Included</td></tr>
                    <tr><td><strong>Preventive Maintenance</strong></td><td>Bi-Monthly Checkup</td><td>Monthly Routine Maintenance</td><td>Weekly Maintenance + 24/7 Remote Monitor</td></tr>
                    <tr><td><strong>Dedicated Tech Engineer</strong></td><td>On-Demand Visit</td><td>Dedicated Resident Engineer</td><td>Team of Resident Engineers</td></tr>
                    <tr><td><strong>Server & Data Backup</strong></td><td>Manual Backup Config</td><td>Daily Automated Cloud Backup</td><td>Real-Time Disaster Recovery Setup</td></tr>
                </tbody>
            </table>
        </div>
        '''
    }
}

for slug, info in data.items():
    cat = ServiceCategory.objects.filter(slug=slug).first()
    if cat:
        cat.learning_video_title = info['title']
        cat.learning_video_url = info['url']
        cat.learning_video_description = info['desc']
        cat.comparison_guide_html = info['guide']
        cat.save()
        print(f'Successfully updated Service Category: {cat.name} ({cat.slug})')
    else:
        print(f'Service Category with slug {slug} not found')

print("Completed Service Categories seeding!")
