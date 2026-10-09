# Website Build and Deployment

The website is a static, dependency-free HTML/CSS/JavaScript site at the repository root.

## Local preview

From the repository root, run:

    python -m http.server 8000

Open http://localhost:8000. The website uses relative links to documentation assets, so preview from the repository root rather than opening index.html directly.

## GitHub Pages

The workflow at .github/workflows/pages.yml validates required assets and deploys the repository root when changes are pushed to main or when manually dispatched.

One-time repository configuration:
1. Open Settings → Pages.
2. Set Build and deployment → Source to GitHub Actions.
3. Merge the website branch into main.
4. Open Actions → Deploy project website to GitHub Pages and inspect the build/deploy result.
5. Use the URL published by the deployment job.

Expected project URL for a standard GitHub Pages project site: https://pui89.github.io/flood-rescue-ai-robot/. This URL is only live after Pages is enabled and a deployment succeeds.

## Validation

The workflow checks required files exist and contain basic HTML/SVG markers. This is a lightweight packaging check, not a full accessibility, security, browser-compatibility or link test. Before public launch, manually test keyboard navigation, small screens, contrast, external links and all documentation links.

## License

The root MIT license covers original website code and assets only to the extent the project owns those rights. Review third-party-licenses.md for dependency, dataset and model-weight policy.