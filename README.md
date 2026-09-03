# McSwain Education Foundation website

Modern, responsive static website for the McSwain Education Foundation. It preserves the public content and assets from the former Weebly site while improving hierarchy, accessibility, mobile behavior, and the donation path.

## Preview locally

```sh
python3 -m http.server 4173 --directory site
```

Then open <http://localhost:4173>.

Run the dependency-free integrity check with:

```sh
python3 scripts/check-site.py
```

## Publish

Pushes to `main` deploy automatically through GitHub Pages after launch is enabled. The repository Pages source must be set to **GitHub Actions**, and the repository variable `PAGES_ENABLED` must be set to `true` once the content is approved for public release.

## Connect a custom domain

1. Choose and purchase the domain.
2. Add it under **Repository settings → Pages → Custom domain**.
3. Configure the registrar DNS records GitHub provides.
4. Turn on **Enforce HTTPS** after DNS verification succeeds.
5. Add the domain name to `site/CNAME` so future deployments retain it.

## Content checks before launch

- Confirm the Foundation contact email. The old site used both `sdonell11@gmail.com` and `sdonnell11@gmail.com`; this rebuild uses the latter.
- Confirm the 2026 Mustang Nights date, venue, schedule, ticket link, and dinner menu.
- Confirm the current board roster and titles.
- Replace or add high-resolution photos when available.

## Source

Public copy, brand artwork, event photography, the event poster, and the 2025 newsletter were migrated from `mcswaineducationfoundation.weebly.com` on September 2, 2026.
