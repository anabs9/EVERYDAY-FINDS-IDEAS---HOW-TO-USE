EVERYDAY FINDS & IDEAS - HOW TO USE

PUBLISH FREE (Cloudflare Pages or Netlify)
1. Create a free account at github.com and make a new repository.
2. Click "Add file > Upload files" and upload everything in this folder (not the zip itself).
3. Create a free account at pages.cloudflare.com (or netlify.com) and choose "Import from GitHub".
4. Select your repository. Build command: python3 build.py   Output folder: dist
5. Click Deploy. You get a free web address; use it in your Pinterest bio.
6. Open site.json and change site_url to that address (and contact_email, pinterest_url). Save and upload again.

ADD A PRODUCT (no coding)
1. Open products.csv in Excel or Google Sheets.
2. Add a row. Set status to "live". Category must be one of: home-finds, kitchen-gadgets, home-organisation, everyday-gadgets, product-recommendations.
3. Fill name, description, problem, features (separate with ;), who, and your Amazon affiliate link in url. Put featured as "yes" to show it on the homepage.
4. Put your own product photo in the images folder and type its file name in the image column.
5. Save as CSV and upload to GitHub, replacing the old file. The site rebuilds in about a minute.

IMAGES: add images/hero.jpg for the homepage and images/cat-home-finds.jpg (and so on for each category). Amazon images may only be used through Amazon's approved tools (such as SiteStripe/Associates image links); do not copy them from product pages.
