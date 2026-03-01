---
title: "From Claude to Cloud: How I Automated My Website Deployment"
date: 2026-03-01
tags: [GCP, ClaudeCode, CICD, CloudRun, WebDev]
author: Anwesha
---

# 🚀 How I Built My Website in a Day Using AI: A Mindset Shift

I have been getting a lot of questions about how I built my website in a single day using AI. As much as it surprises many, I am no different! I never truly imagined how AI could make you this productive and make your work feel so valued until I tried a hands-on project. 

The secret isn't just technical; it’s about being **empathetic, creative,** and thinking through a solution before touching the keyboard (much like how we used to "dry run" code manually before running it on a machine).

---

## 👵 Explaining AI to My Grandma
If I had to explain this process to my grandma, I’d tell her it’s like having a very fast, very eager apprentice in the kitchen. 

* **Brainstorming > Ordering:** You don't just "order" a website like a pizza. You have a conversation. You explain the *vibe*, the goal, and who is coming over for dinner.
* **The "Dry Run":** Before we even turned on the "stove" (the computer), I had to do a manual dry run in my head. If you can't explain the logic of your recipe to yourself, the apprentice is going to burn the toast.
* **Check the Seasoning:** Instead of blindly accepting what the AI does, you have to taste the sauce. Be mindful, check the code, and understand *why* it’s doing what it’s doing. It’s a brainstorming session, not a magic trick.

---

## 🛠 The Tech Stack (The Simple Ingredients)
Based on my repository, here are the tools I used to get the job done:

* **Python & Flask:** The "brain" of the operation that handles the logic.
* **HTML/CSS:** The "skin and clothes" that make the site look professional.
* **Docker:** Think of this as a perfectly packed suitcase. It ensures the website works exactly the same on my laptop as it does on the Google servers.

---

## 🏗 The Architecture: From Laptop to Live
I used **Visual Studio Code** as my workbench. The flow is simpler than you’d think:

1.  **The Push:** I write code and "push" it to the **Git** master branch.
2.  **The Factory:** This triggers **Google Cloud Build**, which automatically starts "baking" the new version of the site.
3.  **The Home:** The site is hosted on **Cloud Run**. It’s brilliant because it only "wakes up" when someone visits the site, making it incredibly efficient.



---

## 🧠 The "Context Window" Secret
I used **Claude Code** to accelerate the build. The real "unlock" here is the **Context Window**. 

Imagine if your apprentice forgot the first half of your sentence by the time you reached the end. That’s a small context window. Claude, however, has a massive "short-term memory." It can "read" my entire project at once—remembering my branding, my previous errors, and my goals—so I never had to repeat myself.

---

## 💻 Technical Deep Dive: The Blueprint
For my fellow engineers, here is the `cloudbuild.yaml` snippet that automates my life. It moves code from my laptop to the world in seconds:

```yaml
steps:
# Step 1: Build the container image
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/anwesha-me', '.']

# Step 2: Push the image to the Registry
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/anwesha-me']

# Step 3: Deploy to Cloud Run
- name: 'gcr.io/[google.com/cloudsdktool/cloud-sdk](https://google.com/cloudsdktool/cloud-sdk)'
  entrypoint: gcloud
  args:
  - 'run'
  - 'deploy'
  - 'anwesha-me'
  - '--image'
  - 'gcr.io/$PROJECT_ID/anwesha-me'
  - '--region'
  - 'australia-southeast1'
```

## 🧗 Challenges & Learning Curves
Even with a super-apprentice, it wasn't all smooth sailing. Here were my biggest hurdles:

The "Yes Man" Trap: AI is incredibly eager to please. If you ask for a complex solution, it will give you one, even if a simple if statement was enough. I had to learn to say, "Let’s keep it simple."

Requirement Drift: If my initial "brain dump" wasn't clear, the AI would hallucinate features I didn't need. I realized that clear requirement gathering is 80% of the battle.

Resisting Blind Trust: It's tempting to just copy-paste and pray. The real challenge was staying mindful and reviewing every line to ensure I actually understood the logic being implemented.

## 💡 The Big Takeaway
My biggest realization? AI doesn't replace the engineer; it elevates you. You stop being the person who just "lays the bricks" and you become the Architect and Director.

When you combine technical "dry runs" with a bit of creative empathy for your user, you aren't just writing code, you are building a solution. You don't need a decade of experience to start; you just need to be clear about what you want to create.

Don't just build code, build a vision that makes you feel valued.