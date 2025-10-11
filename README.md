# githubcontribs: Analyze GitHub contributions across an organization

Install:

```bash
pip install githubcontribs
```

Fetch data:

```python
import githubcontribs
fetcher = githubcontribs.Fetcher("laminlabs")
df = fetcher.run("lamindb")
df.head()
#> Dataframe of contributions
	date		author		repo	type	title											...
0	2025-10-11	falexwolf	lamindb	commit	🚸 Better UX for `lamin annotate` CLI command	...
1	2025-10-10	Koncopd		lamindb	commit	🐛 Various fixes for filtering (#3147)			...
2	2025-10-10	falexwolf	lamindb	commit	🐛 Do not retrieve records from trash based on	...
```

Plot data:

```python
plotter = githubcontribs.Plotter(df)
plotter.plot_total_number_by_author_by_type()
```
<img width="947" height="624" alt="image" src="https://github.com/user-attachments/assets/29a872ac-e244-4ac8-a24f-a66706a20761" />

```python
plotter.plot_number_by_month_by_author()
```
<img width="945" height="624" alt="image" src="https://github.com/user-attachments/assets/cfa31614-352b-469f-bf48-eeaca29cd5dd" />

How to contribute to this repo: Please run `pre-commit install` and `gitmoji -i` on the CLI before starting to work on this repository!
