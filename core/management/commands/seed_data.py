from django.core.management.base import BaseCommand
from core.models import SiteSettings, Testimonial, Page
from products.models import ProductCategory, Brand, Product, ProductSpecification, Marketplace, ProductMarketplaceLink
from services.models import ServiceCategory, Service, ServiceFeature, ServicePackage, CCTVPricing, CCTVPackage


class Command(BaseCommand):
    help = "Seeds initial database records for Nehru Place IT Services"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding process..."))

        # 1. Site Settings
        settings, created = SiteSettings.objects.get_or_create(id=1)
        settings.company_name = "Nehru Place IT Services"
        settings.tagline = "Smart IT Solutions for Modern Business"
        settings.phone = "+91 98765 43210"
        settings.alternate_phone = "+91 11 2641 0000"
        settings.email = "info@nehruplaceitservices.com"
        settings.whatsapp_number = "919876543210"
        settings.address = "Nehru Place IT Hub, Building 42, Commercial Complex, Nehru Place, New Delhi, Delhi 110019"
        settings.google_map_url = "https://maps.google.com/?q=Nehru+Place+New+Delhi"
        settings.facebook_url = "https://facebook.com/nehruplaceitservices"
        settings.instagram_url = "https://instagram.com/nehruplaceitservices"
        settings.linkedin_url = "https://linkedin.com/company/nehruplaceitservices"
        settings.about_text = "Nehru Place IT Services is your trusted premier technology partner based in New Delhi's largest IT hub. We specialize in enterprise IT product supply, custom web application development, HD CCTV security deployment, high-speed office networking, and laptop hardware repair."
        settings.footer_text = "Empowering Delhi NCR & Pan-India businesses with certified IT products, robust security infrastructures, modern responsive web engineering, and prompt technical support."
        settings.default_meta_title = "Nehru Place IT Services | IT Products, Web Dev, CCTV & Support"
        settings.default_meta_description = "Authorized IT products catalog, dynamic web development, CCTV security installation, networking, and laptop repair services in Nehru Place, New Delhi."
        settings.save()
        self.stdout.write(self.style.SUCCESS("[OK] SiteSettings configured."))

        # 2. Product Categories
        cat_data = [
            ("Laptops & Notebooks", "laptops-notebooks", "High performance business and gaming laptops."),
            ("Desktop Computers", "desktop-computers", "Custom desktop PCs, workstations, and all-in-ones."),
            ("CCTV & Security", "cctv-security", "HD CCTV cameras, DVRs, NVRs, and surveillance kits."),
            ("Networking Hardware", "networking-hardware", "Gigabit routers, managed switches, and Wi-Fi 6 access points."),
            ("Computer Components", "computer-components", "Processors, motherboards, RAM modules, and power supplies."),
            ("Storage & Hard Drives", "storage-hard-drives", "High-speed NVMe SSDs, external HDDs, and surveillance storage."),
        ]
        categories = {}
        for name, slug, desc in cat_data:
            c, _ = ProductCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
            categories[slug] = c
        self.stdout.write(self.style.SUCCESS("[OK] Product Categories created."))

        # 3. Brands
        brand_data = [
            ("Dell", "dell"),
            ("HP", "hp"),
            ("Lenovo", "lenovo"),
            ("Hikvision", "hikvision"),
            ("CP PLUS", "cp-plus"),
            ("TP-Link", "tp-link"),
            ("Cisco", "cisco"),
            ("Kingston", "kingston"),
            ("Western Digital", "western-digital"),
            ("Intel", "intel"),
        ]
        brands = {}
        for name, slug in brand_data:
            b, _ = Brand.objects.get_or_create(slug=slug, defaults={'name': name})
            brands[slug] = b
        self.stdout.write(self.style.SUCCESS("[OK] Brands created."))

        # 4. Marketplaces
        mp_data = [
            ("Amazon", "amazon", "https://www.amazon.in", 1),
            ("Flipkart", "flipkart", "https://www.flipkart.com", 2),
            ("Meesho", "meesho", "https://www.meesho.com", 3),
        ]
        marketplaces = {}
        for name, slug, base, order in mp_data:
            m, _ = Marketplace.objects.get_or_create(slug=slug, defaults={'name': name, 'base_url': base, 'sort_order': order})
            marketplaces[slug] = m
        self.stdout.write(self.style.SUCCESS("[OK] Marketplaces created."))

        # 5. Products & Specs & Marketplace Links
        prod1, _ = Product.objects.get_or_create(
            sku="LAP-DELL-5440",
            defaults={
                'name': "Dell Latitude 5440 Laptop (Core i5 13th Gen / 16GB / 512GB SSD / 14\" FHD)",
                'slug': "dell-latitude-5440-laptop",
                'category': categories['laptops-notebooks'],
                'brand': brands['dell'],
                'short_description': "14-inch commercial laptop featuring Intel Core i5 13th Gen, 16GB DDR5 RAM, 512GB NVMe SSD, and Windows 11 Pro.",
                'description': "Dell Latitude 5440 delivers manageable performance and modern enterprise security. Features crisp 14-inch Full HD anti-glare display, backlit keyboard, Wi-Fi 6E, Thunderbolt 4 ports, and long battery life.",
                'price': 78990.00,
                'discount_price': 72490.00,
                'stock_status': 'IN_STOCK',
                'warranty_period': '3 Years',
                'warranty_type': 'Dell On-Site ProSupport Warranty',
                'warranty_details': '3 Years Next Business Day On-Site Warranty covering hardware repairs and remote diagnostic assistance.',
                'warranty_terms': 'Covers manufacturing defects and internal hardware failure. Excludes liquid damage and physical drops unless accidental damage protection is purchased.',
                'featured': True,
                'seo_title': "Buy Dell Latitude 5440 Laptop in Nehru Place | Best Price",
                'seo_description': "Order Dell Latitude 5440 Intel Core i5 13th Gen with 3 Year Onsite Warranty from Nehru Place IT Services.",
            }
        )
        ProductSpecification.objects.get_or_create(product=prod1, specification_name="Processor", defaults={'specification_value': "Intel Core i5-1335U (13th Gen, up to 4.6 GHz)", 'sort_order': 1})
        ProductSpecification.objects.get_or_create(product=prod1, specification_name="RAM", defaults={'specification_value': "16 GB DDR5 (Expandable up to 64 GB)", 'sort_order': 2})
        ProductSpecification.objects.get_or_create(product=prod1, specification_name="Storage", defaults={'specification_value': "512 GB M.2 NVMe PCIe Gen4 SSD", 'sort_order': 3})
        ProductSpecification.objects.get_or_create(product=prod1, specification_name="Display", defaults={'specification_value': "14.0-inch FHD (1920 x 1080) Anti-Glare IPS 250 nits", 'sort_order': 4})
        ProductSpecification.objects.get_or_create(product=prod1, specification_name="Operating System", defaults={'specification_value': "Windows 11 Professional (64-bit)", 'sort_order': 5})
        ProductMarketplaceLink.objects.get_or_create(product=prod1, marketplace=marketplaces['amazon'], defaults={'url': 'https://www.amazon.in/dp/B0C7L8M9NP'})
        ProductMarketplaceLink.objects.get_or_create(product=prod1, marketplace=marketplaces['flipkart'], defaults={'url': 'https://www.flipkart.com/dell-latitude-5440/p/itm123456789'})

        prod2, _ = Product.objects.get_or_create(
            sku="CCTV-HIK-4CH-KIT",
            defaults={
                'name': "Hikvision 4-Camera 2MP Full HD CCTV Surveillance Kit",
                'slug': "hikvision-4-camera-cctv-surveillance-kit",
                'category': categories['cctv-security'],
                'brand': brands['hikvision'],
                'short_description': "Complete 4-camera 1080P HD CCTV system package including 4 Channel DVR, 1TB HDD, cabling & power supply.",
                'description': "Ideal for home, shop, and small office security. Features 2MP night vision bullet & dome cameras, smart motion detection, H.265+ compression, and remote mobile viewing via Hik-Connect app on iOS/Android.",
                'price': 18500.00,
                'discount_price': 15999.00,
                'stock_status': 'IN_STOCK',
                'warranty_period': '2 Years',
                'warranty_type': 'Hikvision Official Warranty',
                'warranty_details': '2 Years warranty on DVR and Cameras, 1 Year warranty on Hard Disk.',
                'warranty_terms': 'Warranty valid with purchase invoice. Does not cover high voltage burnout or cable cut damages.',
                'featured': True,
                'seo_title': "Hikvision 4 Camera CCTV Package Price Delhi | Nehru Place IT",
                'seo_description': "Get Hikvision 4 Camera 2MP HD CCTV kit with installation & mobile app setup from Nehru Place IT Services.",
            }
        )
        ProductSpecification.objects.get_or_create(product=prod2, specification_name="Camera Resolution", defaults={'specification_value': "2 Megapixel 1080P Full HD", 'sort_order': 1})
        ProductSpecification.objects.get_or_create(product=prod2, specification_name="DVR Channels", defaults={'specification_value': "4 Channel H.265+ HD DVR", 'sort_order': 2})
        ProductSpecification.objects.get_or_create(product=prod2, specification_name="Storage Included", defaults={'specification_value': "1 TB Surveillance Grade Hard Disk Drive", 'sort_order': 3})
        ProductSpecification.objects.get_or_create(product=prod2, specification_name="Night Vision", defaults={'specification_value': "Infrared Night Vision up to 20 meters", 'sort_order': 4})
        ProductMarketplaceLink.objects.get_or_create(product=prod2, marketplace=marketplaces['amazon'], defaults={'url': 'https://www.amazon.in/dp/B08XYZ1234'})
        ProductMarketplaceLink.objects.get_or_create(product=prod2, marketplace=marketplaces['meesho'], defaults={'url': 'https://www.meesho.com/s/product-hikvision-cctv-4ch'})

        prod3, _ = Product.objects.get_or_create(
            sku="NET-TPL-AX55",
            defaults={
                'name': "TP-Link Archer AX55 Dual-Band Wi-Fi 6 Router",
                'slug': "tp-link-archer-ax55-wifi-6-router",
                'category': categories['networking-hardware'],
                'brand': brands['tp-link'],
                'short_description': "AX3000 Dual Band Gigabit Wi-Fi 6 Router with Qualcomm CPU, HomeShield, and USB 3.0 port.",
                'description': "Next-gen Wi-Fi 6 speeds up to 3000 Mbps for smooth 4K streaming, gaming, and multi-device office environments. Features 4 high-gain antennas, OFDMA & MU-MIMO technology, and VPN client support.",
                'price': 6999.00,
                'discount_price': 5499.00,
                'stock_status': 'IN_STOCK',
                'warranty_period': '3 Years',
                'warranty_type': 'TP-Link India Replacement Warranty',
                'featured': True,
            }
        )
        ProductSpecification.objects.get_or_create(product=prod3, specification_name="Wi-Fi Standard", defaults={'specification_value': "Wi-Fi 6 (802.11ax)", 'sort_order': 1})
        ProductSpecification.objects.get_or_create(product=prod3, specification_name="Speed", defaults={'specification_value': "AX3000 (2402 Mbps on 5 GHz + 574 Mbps on 2.4 GHz)", 'sort_order': 2})
        ProductSpecification.objects.get_or_create(product=prod3, specification_name="Ports", defaults={'specification_value': "1 Gigabit WAN + 4 Gigabit LAN + 1 USB 3.0", 'sort_order': 3})
        ProductMarketplaceLink.objects.get_or_create(product=prod3, marketplace=marketplaces['amazon'], defaults={'url': 'https://www.amazon.in/dp/B09G96T8M6'})
        ProductMarketplaceLink.objects.get_or_create(product=prod3, marketplace=marketplaces['flipkart'], defaults={'url': 'https://www.flipkart.com/tp-link-ax55/p/itm987654'})

        self.stdout.write(self.style.SUCCESS("[OK] Products & Specs created."))

        # 6. Service Categories
        s_cat_data = [
            ("Website Development", "website-development", "Custom responsive web development, web apps, and e-commerce solutions.", "bi-globe", 1),
            ("CCTV & Security", "cctv-installation", "Commercial & residential CCTV installation, wiring, and maintenance.", "bi-camera-video", 2),
            ("Networking Services", "networking-services", "Structured LAN cabling, Wi-Fi deployment, router & switch setup.", "bi-diagram-3", 3),
            ("Computer Repair", "computer-repair", "Laptop & desktop repair, OS installation, SSD upgrade, data recovery.", "bi-laptop", 4),
            ("IT Support & AMC", "it-support-amc", "Corporate IT helpdesk, Annual Maintenance Contracts, and on-site support.", "bi-headset", 5),
        ]
        s_categories = {}
        for name, slug, desc, icon, order in s_cat_data:
            sc, _ = ServiceCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc, 'icon': icon, 'sort_order': order})
            s_categories[slug] = sc
        self.stdout.write(self.style.SUCCESS("[OK] Service Categories created."))

        # 7. Services & Packages
        srv1, _ = Service.objects.get_or_create(
            slug="static-website-development",
            defaults={
                'name': "Static Website Development",
                'category': s_categories['website-development'],
                'short_description': "Fast, secure, mobile-responsive static website for business portfolios and company profiles.",
                'description': "Professional static website design crafted with HTML5, CSS3, Bootstrap, fast loading animations, contact forms, Google Maps integration, and search engine optimization (SEO).",
                'starting_price': 9999.00,
                'price_unit': "per website",
                'delivery_time': "3-5 Business Days",
                'featured': True,
                'seo_title': "Static Website Development Service in Nehru Place Delhi",
                'seo_description': "Get custom business static website starting at ₹9,999 from Nehru Place IT Services.",
            }
        )
        ServiceFeature.objects.get_or_create(service=srv1, feature_text="Mobile & Tablet Responsive Design", defaults={'sort_order': 1})
        ServiceFeature.objects.get_or_create(service=srv1, feature_text="Fast Page Speed & Clean Code", defaults={'sort_order': 2})
        ServiceFeature.objects.get_or_create(service=srv1, feature_text="WhatsApp & Interactive Lead Forms", defaults={'sort_order': 3})
        ServiceFeature.objects.get_or_create(service=srv1, feature_text="Basic On-Page SEO & Meta Tags", defaults={'sort_order': 4})
        ServiceFeature.objects.get_or_create(service=srv1, feature_text="1 Year Free Hosting & Domain Setup Support", defaults={'sort_order': 5})

        ServicePackage.objects.get_or_create(
            service=srv1, name="Basic Static",
            defaults={
                'description': "Essential 5-page business site.",
                'price': 9999.00,
                'features': "Up to 5 Pages\nResponsive Mobile Design\nContact Form\nGoogle Map Setup\nWhatsApp Chat Button\nDelivery in 3 Days",
                'delivery_days': "3 Days",
                'sort_order': 1
            }
        )
        ServicePackage.objects.get_or_create(
            service=srv1, name="Standard Static",
            defaults={
                'description': "Comprehensive 10-page corporate website.",
                'price': 14999.00,
                'is_featured': True,
                'features': "Up to 10 Pages\nResponsive Mobile Design\nProduct Gallery / Portfolio\nAdvanced Enquiry Form\nSEO Optimization\nSocial Media Links\nDelivery in 5 Days",
                'delivery_days': "5 Days",
                'sort_order': 2
            }
        )
        ServicePackage.objects.get_or_create(
            service=srv1, name="Premium Static",
            defaults={
                'description': "Full corporate portal with up to 20 pages.",
                'price': 24999.00,
                'features': "Up to 20 Pages\nCustom UI/UX Theme\nDynamic Contact & Quote Forms\nSpeed Optimization (< 2s load)\nGoogle Analytics & Console Setup\n1 Year Priority Maintenance\nDelivery in 7 Days",
                'delivery_days': "7 Days",
                'sort_order': 3
            }
        )

        srv2, _ = Service.objects.get_or_create(
            slug="dynamic-website-development",
            defaults={
                'name': "Dynamic Website & Web Application",
                'category': s_categories['website-development'],
                'short_description': "Custom Python / Django powered web applications, CMS portals, and database systems.",
                'description': "Full-stack dynamic web development utilizing Django framework and MySQL. Includes admin dashboard, dynamic content management, secure user roles, lead processing, and custom API integrations.",
                'starting_price': 24999.00,
                'price_unit': "per portal",
                'delivery_time': "7-14 Business Days",
                'featured': True,
            }
        )
        ServiceFeature.objects.get_or_create(service=srv2, feature_text="Django + MySQL Backend Architecture", defaults={'sort_order': 1})
        ServiceFeature.objects.get_or_create(service=srv2, feature_text="Custom Admin Management Dashboard", defaults={'sort_order': 2})
        ServiceFeature.objects.get_or_create(service=srv2, feature_text="Database-Driven Products & Services", defaults={'sort_order': 3})
        ServiceFeature.objects.get_or_create(service=srv2, feature_text="Secure Authentication & Role Permissions", defaults={'sort_order': 4})

        srv3, _ = Service.objects.get_or_create(
            slug="cctv-installation-service",
            defaults={
                'name': "CCTV Sales & Professional Installation",
                'category': s_categories['cctv-installation'],
                'short_description': "End-to-end HD & IP camera installation for offices, retail stores, warehouses, and homes.",
                'description': "Complete CCTV security installation including camera mounting, structured conduit wiring, DVR/NVR configuration, router port forwarding, and smartphone live streaming setup.",
                'starting_price': 1500.00,
                'price_unit': "starting per camera",
                'delivery_time': "1-2 Days",
                'featured': True,
            }
        )

        srv4, _ = Service.objects.get_or_create(
            slug="computer-laptop-repair",
            defaults={
                'name': "Laptop & Computer Hardware Repair",
                'category': s_categories['computer-repair'],
                'short_description': "Chip-level laptop repair, screen replacement, SSD speed upgrade, motherboard fix, and OS formatting.",
                'description': "Fast, reliable computer repair services in Nehru Place. We fix broken laptop hinges, cracked LED screens, slow booting issues, keyboard defects, and motherboard liquid damage.",
                'starting_price': 499.00,
                'price_unit': "per diagnosis",
                'delivery_time': "Same Day / 24 Hours",
                'featured': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Services & Features created."))

        # 8. CCTV Pricing Defaults
        cctv_pricing = CCTVPricing.get_pricing()
        cctv_pricing.camera_price = 2000.00
        cctv_pricing.dvr_nvr_price = 5000.00
        cctv_pricing.hdd_price = 4000.00
        cctv_pricing.power_supply_price = 800.00
        cctv_pricing.connector_price = 300.00
        cctv_pricing.cable_price_per_meter = 25.00
        cctv_pricing.installation_charge = 2000.00
        cctv_pricing.wiring_charge_per_meter = 15.00
        cctv_pricing.configuration_charge = 1000.00
        cctv_pricing.maintenance_charge = 1500.00
        cctv_pricing.save()
        self.stdout.write(self.style.SUCCESS("[OK] CCTV Pricing updated."))

        # 9. CCTV Preset Packages
        CCTVPackage.objects.get_or_create(
            name="4-Camera HD Home/Shop Setup",
            defaults={
                'camera_count': 4,
                'camera_type': "2MP Full HD Indoor/Outdoor Night Vision Bullet",
                'dvr_nvr': "4 Channel H.265+ DVR",
                'storage': "1 TB Surveillance HDD",
                'cable_meters': 100,
                'installation_charge': 2000.00,
                'wiring_charge': 1500.00,
                'other_charge': 0.00,
                'package_price': 21500.00,
                'description': "Complete 4 camera security package with 100m wiring, installation, and mobile phone app configuration.",
                'is_active': True,
            }
        )
        CCTVPackage.objects.get_or_create(
            name="8-Camera Office & Commercial Kit",
            defaults={
                'camera_count': 8,
                'camera_type': "2MP Full HD Dome & Bullet Combo",
                'dvr_nvr': "8 Channel H.265+ HD DVR",
                'storage': "2 TB Surveillance HDD",
                'cable_meters': 200,
                'installation_charge': 3500.00,
                'wiring_charge': 3000.00,
                'other_charge': 500.00,
                'package_price': 38500.00,
                'description': "Comprehensive 8 camera setup for commercial offices, warehouses, and showrooms.",
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] CCTV Preset Packages created."))

        # 10. Testimonials
        Testimonial.objects.get_or_create(
            customer_name="Rajesh Kumar",
            defaults={
                'company': "Apex Logistics Pvt Ltd",
                'designation': "Operations Manager",
                'rating': 5,
                'review': "Nehru Place IT Services provided complete CCTV setup and office LAN networking for our new 30-workstation office. Professional team, clean wiring, and great ongoing support!",
                'is_featured': True,
            }
        )
        Testimonial.objects.get_or_create(
            customer_name="Pooja Sharma",
            defaults={
                'company': "Vogue Fashion Studio",
                'designation': "Founder",
                'rating': 5,
                'review': "They built our e-commerce portal in record time. The Django backend is super smooth to manage products, and their technical response time is unbeatable.",
                'is_featured': True,
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Testimonials created."))

        # 11. CMS Pages
        Page.objects.get_or_create(
            slug="about",
            defaults={
                'title': "About Nehru Place IT Services",
                'content': """<h3>Your Trusted IT Partner in New Delhi</h3>
<p>Located in the heart of Nehru Place — Asia's premier computer and technology hub — <strong>Nehru Place IT Services</strong> has been delivering cutting-edge technology products, custom web development, CCTV security solutions, and enterprise networking services to businesses and individual customers.</p>
<h4>Our Key Core Capabilities:</h4>
<ul>
  <li>Genuine IT Products catalog with direct marketplace purchasing links.</li>
  <li>Custom Python/Django dynamic websites and scalable web applications.</li>
  <li>HD & IP CCTV surveillance setup with remote mobile live viewing.</li>
  <li>Structured LAN & Wi-Fi office networking installation.</li>
  <li>Rapid chip-level laptop repair and hardware upgrades.</li>
</ul>""",
                'seo_title': "About Us | Nehru Place IT Services",
                'seo_description': "Learn about Nehru Place IT Services - leading IT products seller, web development company, CCTV installer, and laptop repair service provider in Nehru Place.",
            }
        )

        Page.objects.get_or_create(
            slug="privacy-policy",
            defaults={
                'title': "Privacy Policy",
                'content': "<p>We value customer privacy. Any information submitted via forms or enquiries is strictly used for technical assistance and service response.</p>",
                'seo_title': "Privacy Policy | Nehru Place IT Services",
            }
        )

        Page.objects.get_or_create(
            slug="terms-and-conditions",
            defaults={
                'title': "Terms & Conditions",
                'content': "<p>Standard service and product supply terms apply. Hardware warranties are backed by official manufacturer policies.</p>",
                'seo_title': "Terms & Conditions | Nehru Place IT Services",
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] CMS Pages created."))

        # 12. Default Admin Superuser Creation & Reset
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@nehruplaceitservices.com', 'is_staff': True, 'is_superuser': True})
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("[OK] Admin Superuser set (Username: admin | Password: admin123)."))

        self.stdout.write(self.style.SUCCESS("ALL SEED DATA POPULATED SUCCESSFULLY!"))

