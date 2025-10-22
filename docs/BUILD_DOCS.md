# lifeActuary Documentation

This directory contains the complete MkDocs documentation for the lifeActuary package.

## Quick Start

### 1. Install Dependencies

```bash
# On macOS/Linux
./build-docs.sh install

# On Windows
build-docs.bat install

# Or manually
pip install -r requirements-docs.txt
```

### 2. Serve Locally (Development)

```bash
# On macOS/Linux
./build-docs.sh serve

# On Windows
build-docs.bat serve

# Or manually
mkdocs serve
```

Then open http://localhost:8000 in your browser.

### 3. Build for Production

```bash
# On macOS/Linux
./build-docs.sh build

# On Windows
build-docs.bat build

# Or manually
mkdocs build
```

### 4. Deploy to GitHub Pages

```bash
# On macOS/Linux
./build-docs.sh deploy

# On Windows
build-docs.bat deploy

# Or manually
mkdocs gh-deploy
```

## Documentation Structure

```
docs/
├── index.md                      # Home page
├── user-guide/
│   ├── installation.md           # Installation instructions
│   ├── quick-start.md            # Quick start guide
│   └── tutorials.md              # Step-by-step tutorials
├── api/
│   ├── mortality_table.md        # Mortality tables API
│   ├── annuities.md              # Life annuities API
│   ├── annuities_certain.md      # Annuities certain API
│   ├── annuities_rv.md           # Annuities random variables API
│   ├── mortality_insurance.md    # Life insurance API
│   ├── mortality_insurance_frac.md # Fractional insurance API
│   ├── mortality_rv.md           # Mortality random variables API
│   ├── commutation_table.md      # Commutation tables API
│   ├── commutation_table_frac.md # Fractional commutation API
│   ├── life_2heads.md            # Two lives functions API
│   └── mortality_table_2heads.md # Two lives mortality tables API
├── examples/
│   ├── basic.md                  # Basic examples
│   ├── advanced.md               # Advanced examples
│   └── soa_tables.md             # SOA tables examples
└── about/
    ├── release-notes.md          # Release notes and changelog
    └── license.md                # License and disclaimer
```

## Features

- **Material Design Theme**: Modern, responsive design
- **Search**: Full-text search across all documentation
- **Code Highlighting**: Syntax highlighting for Python code
- **Math Support**: LaTeX math rendering with MathJax
- **API Documentation**: Auto-generated from docstrings using mkdocstrings
- **Dark/Light Mode**: Theme toggle
- **Mobile Friendly**: Responsive design for all devices

## Configuration

The documentation is configured through `mkdocs.yml`:

- **Theme**: Material theme with custom colors
- **Plugins**: Search, mkdocstrings for API docs
- **Extensions**: Python Markdown extensions for enhanced formatting
- **Math**: MathJax for mathematical notation
- **Navigation**: Organized hierarchical structure

## Writing Documentation

### Markdown Files

Documentation is written in Markdown with these extensions:

- **Admonitions**: Note, warning, tip boxes
- **Code Blocks**: Syntax highlighted code
- **Tables**: Formatted tables
- **Math**: LaTeX mathematical notation
- **Links**: Cross-references between pages

### API Documentation

API documentation is automatically generated from Python docstrings using the mkdocstrings plugin:

```markdown
::: lifeActuary.mortality_table.MortalityTable
```

### Code Examples

Include runnable Python code examples:

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 1.0])

# Calculate annuity
result = annuities.ax(mt, x=1, i=5)
print(f"Annuity value: {result:.4f}")
```

### Mathematical Notation

Use LaTeX for mathematical formulas:

- Inline: `$a_x = \frac{N_x}{D_x}$`
- Block: `$$a_x = \sum_{k=0}^{\infty} {}_kp_x v^k$$`

## Deployment

### GitHub Pages

The documentation can be automatically deployed to GitHub Pages:

1. Ensure your repository has GitHub Pages enabled
2. Run `mkdocs gh-deploy` to deploy to the `gh-pages` branch
3. Documentation will be available at `https://username.github.io/repository-name/`

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to the `docs/` directory with your domain
2. Configure DNS to point to GitHub Pages
3. Enable custom domain in repository settings

### CI/CD

For automatic deployment on push, create `.github/workflows/docs.yml`:

```yaml
name: docs
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.x
      - run: pip install -r requirements-docs.txt
      - run: mkdocs gh-deploy --force
```

## Maintenance

### Adding New Content

1. Create new Markdown files in appropriate directories
2. Update navigation in `mkdocs.yml`
3. Test locally with `mkdocs serve`
4. Build and deploy

### Updating API Documentation

API documentation is generated from docstrings. To update:

1. Improve docstrings in Python source code
2. Regenerate documentation
3. Review and test changes

### Checking Links

Regularly check for broken links:

```bash
# Install linkchecker
pip install linkchecker

# Check built site
mkdocs build
linkchecker site/
```

## Troubleshooting

### Common Issues

**Missing Dependencies**
```bash
pip install -r requirements-docs.txt
```

**Port Already in Use**
```bash
mkdocs serve --dev-addr=127.0.0.1:8001
```

**Build Errors**
- Check YAML syntax in `mkdocs.yml`
- Verify all referenced files exist
- Check Python import paths

**Deployment Issues**
- Ensure GitHub Pages is enabled
- Check repository permissions
- Verify branch settings

### Getting Help

- Check MkDocs documentation: https://www.mkdocs.org/
- Material theme docs: https://squidfunk.github.io/mkdocs-material/
- mkdocstrings plugin: https://mkdocstrings.github.io/

## Contributing

When contributing to documentation:

1. Follow the existing structure and style
2. Test changes locally before submitting
3. Include examples for new features
4. Update navigation if adding new pages
5. Check spelling and grammar
6. Ensure code examples are correct and executable