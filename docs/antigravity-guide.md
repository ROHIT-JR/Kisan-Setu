# Google Antigravity — Complete Setup & Usage Guide
### For the Kisan Setu team · Hackathon build, Sept 2026

**Who this is for:** the team member without a Claude subscription, or anyone who'd rather not use theirs. No prior experience assumed. If you can install an app and type instructions in English, you can use this.

**Time to get running: about 20 minutes.**

---

## PART A — WHAT ANTIGRAVITY ACTUALLY IS

### The one-sentence version
Antigravity is Google's free AI coding tool where you **describe what you want in plain English and an AI agent writes the code, runs it, tests it, and fixes its own mistakes** — instead of you typing every line.

### How it's different from ChatGPT or Gemini in a browser
| Chatbot in a browser | Antigravity |
|---|---|
| You ask, it answers, you copy-paste into your editor | It writes files directly into your project |
| Can't run your code | Runs commands, sees the errors, fixes them |
| Forgets your project between chats | Reads your whole codebase for context |
| One conversation at a time | Up to **five agents working in parallel** on different tasks |
| Can't see your app | Opens Chrome, clicks through your UI, reports what broke |

That last one matters for us: our deliverable is a **live web app**, and Antigravity can actually open it in a browser and verify it works.

### The essentials
- Built on a modified fork of **Visual Studio Code**, so it looks like a normal code editor
- Launched November 2025 alongside Gemini 3
- **Free during public preview** — no credit card, personal Gmail is enough
- Free users get **Gemini 3 Pro** and unlimited tab completions
- Two main views: **Editor** (normal coding) and **Manager** (mission control for agents), toggled with `Cmd+E` / `Ctrl+E`

### The one catch: quota
Agent requests are rate-limited. Google moved free users to a **weekly** allowance rather than a daily one, and usage tracks the *work the agent does* — a complex reasoning task eats far more than a simple edit.

**What this means for you practically:**
- Do your hardest thinking **early in the week** while quota is fresh
- Don't burn requests on things you could type yourself in two minutes
- If you hit the wall mid-week, switch to Editor view and code manually — the editor itself keeps working

---

## PART B — INSTALLATION (15 minutes)

### Step 1 — Download
Go to **`antigravity.google/download`**.

You'll see several options. **Take the desktop client.** It bundles the Agent Manager, the editor, and the browser integration into one app. The other options (standalone IDE, VS Code/JetBrains/Zed extensions, CLI, Python SDK) are for teams already committed to another editor — that's not us.

Pick the installer for your OS. On Mac, choose the right chip (Apple Silicon vs Intel).

### Step 2 — Run the installer
Standard install. Nothing unusual.

### Step 3 — First launch questions
It asks a short series of setup questions. Answer and click Next through each:

1. **Import settings?** → Choose **"Start fresh"** unless you already use VS Code and want your settings carried over.
2. **Theme** → Whatever you like. Cosmetic.
3. **Sign in** → Use a **personal Gmail account**. This opens your browser; approve, and it returns you to the app.
4. **Terms of use** → Read, decide on the opt-in, click Next.

### Step 4 — The important screen: autonomy mode
You'll see the Agent Manager configuration with three development modes. This is asking *"how much should the AI do without asking you first?"*

| Mode | What happens | Use it? |
|---|---|---|
| **Agent-driven** | Full autopilot. Writes files and runs commands without asking. | ❌ Not at first |
| **Review-driven** | Asks permission before almost every action. | ✅ **Start here** for your first day |
| **Agent-assisted** | You stay in control; it handles safe automations itself. | ✅ **Switch here** once you trust it |

**Our recommendation:** start on **Review-driven** for your first task so you can see what it's doing. Move to **Agent-assisted** after that — it's the sane default. Avoid full Agent-driven on a hackathon repo where a bad autonomous decision costs you hours.

### Step 5 — Browser integration
Antigravity integrates with Chrome so agents can open and test your app. Follow the prompt to install the Chrome extension. **Do this** — it's how the agent verifies our live deployment actually works.

---

## PART C — THE TWO VIEWS

Toggle between them with **`Cmd+E`** (Mac) / **`Ctrl+E`** (Windows/Linux).

### Editor view
Looks and works like VS Code. Your file tree on the left, code in the middle. Use it to read what the agent wrote, make small edits yourself, and check things over.

**Useful trick:** in the Problems panel, hover any error and click **"Explain and Fix"** to send it to the agent. There's also **"Send all to Agent"** to batch-fix several at once. In the terminal, select error output and press **`Cmd+L`** to send it straight to the agent.

### Manager view
Mission control. You create tasks, watch agents work, and review what they produced. You can run **up to five agents in parallel**, each in its own workspace.

**For our project: don't run five agents.** One task at a time, reviewed before the next. Parallel agents on a shared repo create merge conflicts you don't have time to untangle.

---

## PART D — YOUR FIRST TASK (do this before touching the real repo)

Prove the tool works before trusting it with the hackathon code.

1. Create an empty folder anywhere, e.g. `antigravity-test`
2. Open Antigravity → open that folder
3. Go to **Agent Manager** → select the folder → click **New Task**
4. Paste this:

```
Create a simple Python script that prints the first 20 Fibonacci numbers.
Then create a README.md explaining how to run it.
Run the script and confirm the output is correct.
```

5. Watch it work. It should write the file, run it, and show you the output.

If that works, you're set up correctly. Delete the folder and move on.

---

## PART E — WORKING ON THE KISAN SETU REPO

### Step 1 — Clone the repo
In Antigravity's terminal (or your own):
```bash
git clone https://github.com/ROHIT-JR/Kisan-Setu.git
cd Kisan-Setu
```
Then open that folder in Antigravity.

### Step 2 — Give the agent the project context
**This is the single most important step, and the easiest one to skip.**

Antigravity supports an **`AGENTS.md`** file at the repo root that acts as standing instructions the agent reads on every task. Create it:

```bash
# from the repo root
cp prompt.md AGENTS.md
```

Or create `AGENTS.md` manually with at minimum:

```markdown
# Project rules — read before every task

Read prompt.md and track4-execution-package.md for full context.

## Hard constraints
- Budget is ₹0. Never use Vertex AI, Gemini Pro models, Cloud SQL,
  Cloud Load Balancer, or Cloud Translation/Speech at runtime.
- Never quote a single accuracy number without both the lab (PlantVillage)
  and field (PlantDoc) columns.
- Any synthetic/mock data must carry `synthetic: true` in API responses
  AND be visibly flagged in the UI.
- Module B is a RULES ENGINE WITH LLM NARRATION — never describe it as a
  trained predictive model.
- Every record carries state_code, district_code, block_code (LGD codes).
- No secrets in the repo. This repository is public.
```

### Step 3 — Start a task
Agent Manager → **New Task**. Write your instruction referencing the issue you're assigned.

---

## PART F — HOW TO WRITE A GOOD TASK PROMPT

The quality of what you get back is almost entirely determined by how you ask.

### ❌ Bad
```
build the advisory API
```
Too vague. The agent invents requirements, you get something unusable, and you've burned quota.

### ✅ Good
```
Read prompt.md sections 5 (MODULE B) and 12 (API CONTRACTS).

Implement backend/app/routers/advisory.py and
backend/app/services/rotation_engine.py for GitHub Issue #7.

Requirements:
- POST /api/advisory accepts { district_code, crop, season, lang }
- Response must match the exact schema in prompt.md §12
- rotation_engine.py is a DETERMINISTIC rules engine reading from
  crop_rotation_rules.yaml — not a trained model
- Rules to encode: low organic carbon -> cover crop + FYM;
  low N + cereal history -> legume rotation; high EC -> salinity management
- Every recommendation must include a `rationale` and an `evidence` array
  naming which soil/NDVI fields drove it
- Gemini narration layer comes after the rules output, not instead of it

Do not implement the Earth Engine calls — that's issue #5, already done.
Import from services/earth_engine.py.

Ask me before making any assumption about agronomy thresholds.
```

### The five-part formula
1. **Point it at the source of truth** — "read prompt.md §5 and §12"
2. **Name the exact files** to create or change
3. **State the acceptance criteria** — what "done" means
4. **State what NOT to do** — scope boundaries prevent the agent wandering
5. **Tell it to ask rather than guess** on anything ambiguous

---

## PART G — THE FOUR RULES THAT MATTER MOST

**1. Review every diff before accepting.**
Agents write plausible-looking code that's subtly wrong. Read what changed. This is not optional on a repo four people share.

**2. Commit after every working task.**
```bash
git add -A && git commit -m "feat: advisory rules engine (#7)"
```
If the next task goes sideways, `git checkout .` costs you nothing.

**3. One task at a time.**
Antigravity can run five agents in parallel. On a shared hackathon repo, don't. Merge conflicts at 2am on Day 10 are how teams miss deadlines.

**4. Pull before you start, push when you finish.**
```bash
git pull origin main    # before
git push origin main    # after
```
Three other people are working in this repo.

---

## PART H — YOUR SPECIFIC ASSIGNMENT

> Fill in your role below and delete the rest.

### If you're M4 (Product/Evaluation) — recommended Antigravity slot
**Issues #11, #12, #13**

This is the best fit for Antigravity: heavy reasoning, low volume, comfortably inside a weekly quota. Gemini 3 Pro handles the docs and deck framing well, and the browser integration helps with research.

**Your highest-value contribution is Issue #13 (adversarial review).** Because you're on a different model family than the other three, you catch what Claude's blind spots miss. Point Gemini 3 Pro at the code the others wrote and ask it to attack the claims. Run the ten questions in §13 of `prompt.md`.

Suggested task prompt:
```
Read prompt.md, especially §9 (LANGUAGE DISCIPLINE) and §13.

Review the entire repository as a hostile hackathon judge. For each of
the ten questions in §13, find the answer in the code and tell me where
it's weak. Specifically flag:
- any accuracy number quoted without both columns
- any synthetic data not flagged as synthetic
- any claim of capability the code does not support
- any Vertex AI or Gemini Pro usage

Output a table: issue, file, line, severity, suggested fix.
```

### If you're M3 (Full-Stack/Deployment)
**Issues #1, #8, #9, #10**

Good fit — mostly boilerplate, and the Chrome integration genuinely helps because you can have the agent open the deployed URL and verify it renders. Start with Issue #1; nothing else matters until the live URL exists.

### If you're M2 (Geospatial/Data) — highest risk slot
**Issues #5, #6, #7**

Gemini 3 Pro is actually the *best* model for Earth Engine work — it's Google's own model on Google's own platform. But #5 and #7 are the two heaviest issues in the project and your quota is weekly.

**Mitigation: front-load.** Spend Monday, while quota is fresh, getting the agent to settle:
- the exact cloud-masking approach for `COPERNICUS/S2_SR_HARMONIZED`
- the full structure of `crop_rotation_rules.yaml`

Save those decisions to files. Then implement from them yourself for the rest of the week without burning agent requests.

### If you're M1 (ML/Vision)
**Issues #2, #3, #4**

Note that training happens on **Google Colab**, not in Antigravity. Use Antigravity for the code and the PlantDoc class-mapping reasoning; run the notebooks on Colab's free T4 GPU.

---

## PART I — TROUBLESHOOTING

| Problem | Fix |
|---|---|
| Hit the quota wall | Switch to Editor view and code manually — the editor keeps working. Quota resets weekly. |
| Agent wrote something wrong | `git checkout .` to discard, then rewrite the prompt more specifically |
| Agent keeps ignoring the ₹0 rule | Your `AGENTS.md` isn't being read. Check it's at the repo root, and repeat the constraint in the task prompt itself |
| Browser integration not working | Reinstall the Chrome extension; make sure Chrome is your default browser |
| Agent is going off-scope | Add explicit "do NOT touch these files" lines to your prompt |
| Merge conflict | Stop. Ask the team before resolving. Don't force-push. |

---

## PART J — QUICK REFERENCE

```
Download           antigravity.google/download
Official tutorial  codelabs.developers.google.com/getting-started-google-antigravity
Toggle views       Cmd+E / Ctrl+E
Send error to agent  Cmd+L (from terminal selection)
Autonomy mode      Settings → start on Review-driven, move to Agent-assisted
Project rules      AGENTS.md at repo root
Repo               github.com/ROHIT-JR/Kisan-Setu
```

**Daily habit:** `git pull` → one task → review the diff → `git commit` → `git push` → post the live URL in the team chat.

---

*Note: Antigravity is in public preview. Free-tier limits and model availability have already changed since launch and may change again. If something in this guide doesn't match what you see, trust what's on screen and tell the team.*
