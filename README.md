# Vue Storefront for Odoo
![Logo](docs/vuepress/public/logo.png)

## Why Odoo?
In contrast of eCommerce integration solutions, Odoo is unique in that it includes ERP, eCommerce and CMS functionalities without the need for additional solutions. As explained in the official website, Odoo is a suite of open-source business apps that cover all the company needs: CRM, eCommerce, accounting, inventory, point of sale, project management, etc. All in all, Odoo's unique value proposition is to be at the same time very easy to use and fully integrated.

## Why Vue Storefront?

Vue Storefront offers a mobile native-like user experience:

- A look and feel that is integrated with the native platform, which implies:
  - An app icon on the home screen.
  - App is able to run full screen.
- A decrease in loading times after the app installs the Service Workers, thanks to caching layouts and content. The mobile app tries to act as immediately as possible on user input, avoiding the use of the internet connection as much as possible.
- Re-engaging with users via push notifications.

Vue Storefront avoids the complexity of having to maintain several native developments – for instance, one for Android and one for iOS –, having a single platform to avoid extra development costs. Furthermore, with the possibility of enabling Server-Side Rendering for the load of the first webpage, we can remark the importance of SEO within the eCommerce industry and offer a solution capable of being crawled by search engines.

## Installation
1. `cd C:\Program Files (x86)\Odoo 12.0\server\odoo\addons`
2. `git clone https://github.com/cristian-g/restful.git restful`
3. Update apps/modules list
![List](docs/vuepress/public/list.png)
![Update list](docs/vuepress/public/update_list.png)
4. Install module
![Install](docs/vuepress/public/install.png)
![Installed](docs/vuepress/public/installed.png)
## Class diagram
![Class diagram](docs/vuepress/public/class_diagram.png)
## Architecture
![Architecture](docs/vuepress/public/architecture.png)

