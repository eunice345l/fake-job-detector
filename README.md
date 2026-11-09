Fake Job Detector



\[!\[Tests](https://github.com/eunice345l/fake-job-detector/actions/workflows/tests.yml/badge.svg)](https://github.com/eunice345l/fake-job-detector/actions/workflows/tests.yml)



A web app that checks a job post or recruiter message and shows how likely it is

to be a scam, with the reasons. Paste the text, click Check, and get a risk level

(low, medium or high), a score out of 100, and a list of warning signs.



How it works



The score combines two parts:



1\. \*\*Rule checks\*\* (`app/rules.py`): simple, explainable warning signs, such as

&#x20;  asking for money, using a free email address (Gmail, Yahoo), contacting only

&#x20;  through WhatsApp or Telegram, pressure to act fast, and unrealistic promises.

&#x20;  Each rule adds points and explains why.

2\. \*\*A machine learning model\*\* (`train.py`): TF-IDF text features with logistic

&#x20;  regression, trained on a public dataset of real and fake job postings.



`app/scorer.py` combines both into one score, and `app/main.py` serves it through

a FastAPI backend with a simple web page.



Results



The model was trained on the Kaggle "Real / Fake Job Posting Prediction" dataset

(17,880 postings, 866 of them fake) and tested on a held-out 20%. Results for the

fake class:



| Method     | Precision | Recall | F1   |

|------------|-----------|--------|------|

| Rules only | 0.00      | 0.00   | 0.00 |

| Model only | 0.74      | 0.90   | 0.81 |

| Combined   | 0.97      | 0.67   | 0.79 |



I report precision, recall and F1 and not accuracy, because only about 5% of the

data is fake, so a model that always answers "real" would score about 95% accuracy

without catching any scams.



What I learned from these results



\- The rules scored zero on this dataset. Its fake postings are mostly polished

&#x20; staffing-style ads, and don't ask for fees or WhatsApp contact, which is what

&#x20; the rules look for.

\- The "Combined" row mostly reflects a stricter cut-off on the model. When I

&#x20; raised the model-only threshold to 0.83, it gave almost the same numbers

&#x20; (precision 0.97, recall 0.66, F1 0.79). So on this data, the rules do not

&#x20; improve the result.

\- Because the dataset doesn't cover the scams the rules target, I tested the

&#x20; rules separately with handwritten scam and genuine messages

&#x20; (`tests/test\_scorer.py`).

\- A bug found through testing: the first version of the fee rule flagged

&#x20; "There is no application fee" as a scam. It now ignores phrases that follow

&#x20; "no" or "without".



Limitations



\- The dataset is from 2012 to 2014 and is mostly English job ads, so it may not

&#x20; reflect today's scams, especially short WhatsApp or Telegram messages.

\- The rule lists and weights are hand-picked and cover only some scam patterns.

\- The result is a warning sign, not proof. It will make mistakes in both

&#x20; directions: some scams will pass and some real posts will be flagged.

\- Never pay money to get a job, whatever the score says.



Run it locally



Requires Python 3.10 or newer.



```bash

git clone https://github.com/eunice345l/fake-job-detector.git

cd fake-job-detector

python -m venv venv

venv\\Scripts\\activate          # Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --reload

```



Open http://127.0.0.1:8000 in your browser.



The trained model (`model.joblib`) is included in the repository. To retrain it,

download `fake\_job\_postings.csv` from the

\[Kaggle dataset](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction),

put it in the `data/` folder, and run `python train.py`.



Run the tests



```bash

python -m pytest

```



The tests also run automatically on every push with GitHub Actions.



Project structure



```

app/

&#x20; rules.py       rule-based scam checks

&#x20; scorer.py      combines the rules and the model

&#x20; main.py        FastAPI backend

&#x20; static/        web page

tests/           pytest tests for the rules, the scorer and the API

explore.py       looks at the dataset

train.py         trains and saves the model

evaluate.py      compares rules, model and combined score

```



Tech



Python, FastAPI, scikit-learn, pandas, pytest, GitHub Actions.



Status



In progress: Docker and deployment are still to be added.



Data



Dataset: "Real / Fake Job Posting Prediction" on Kaggle, from the University of

the Aegean. The data file is not included in this repository.

