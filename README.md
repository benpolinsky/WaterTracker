# WaterTracker

Simple app prototyped with Repl.it. Visualization and analysis of daily water usage.

## Getting Started

```python
python3 -m pip install numpy pandas plotly scipy streamlit trafilatura
streamlit run src/main.py
```


## Notes on Barking Orders At LLMs

Repl.it isn't bad. I imagine it used python because I asked for some data-viz/processing/analysis. Got stuck on csv headings for way too long. It had regrouped the data under different columns, but then was attempting to validate against the original names. Not sure it would have ever fixed the issue on its own - I had to debug the code myself - though it did do some print debugging for me.

GH Copilot (GPT-4o) struggled. I imagine the more-recent models would be more successful, but I couldn't turn my mind off and bark orders at it like I mostly could for repl.it. It's funny, I find my brain going into different modes. I had to snap out of dictate mode and get back into code-analysis mode to make some progress.