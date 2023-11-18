import re
from django.shortcuts import render
from django.http import JsonResponse
import openai
import fitz
from .forms import ResumeUploadForm
from .github import GitHub
import copy
import os
import json

def extract_links(request, text):
    # Use a regular expression to find URLs in the text
    summarized_resume = copy.deepcopy(text)
    url_pattern = re.compile(r'https?://github\S+')
    links = re.findall(url_pattern, text)
    print(links)
    
    if len(links) > 1:
        github = GitHub(links[0])
        github.api()  # Call the GitHub API analysis
        return github.result  # Return the GitHub analysis result
    else:
        return None
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=generate_resume_summarization_task(summarized_resume),
        max_tokens=500,
    )
    ai_summary = response.choices[0].text.strip()
    return render(request, 'summary.html', {'ai_summary': ai_summary})

def generate_resume_summarization_task(resume_summary):
    task_template = f"""
    **Task: Machine Test**

    ---

    **Description:**

    Recruiters often need to give some task to verify candidate knowledge

    **Input:**

    Provide a resume summary generated using openai.

    **Output:**

    The system should generate a task according to candidate skills:

    **Example Input:**

    ```
    {resume_summary}
    """
    return task_template.strip()

def analyze_resume(request):
    form = ResumeUploadForm()

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():

            resume_pdf = form.cleaned_data['resume_pdf']

            doc = fitz.open(resume_pdf)
            resume_text = ""
            for page in doc.pages():
                resume_text += page.get_text()

            job_description = form.cleaned_data['job_description']

            openai.api_key = os.environ.get("OPENAI_API_KEY")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"\n Conduct a comprehensive analysis of the individual’s profile, taking into account all the information provided. This should include an evaluation of their educational background, work history, skills, and notable achievements. Be sure to also examine any links included in the resume for additional information, especially those leading to professional networking sites like LinkedIn, or repositories showcasing their work, such as GitHub. Identify any potential areas of concern or exceptional strengths. Consider their career progression and how their experiences align with their goals. Also, assess their potential for growth and adaptability in various contexts. Remember to scrape all the links in the resume, particularly those to LinkedIn, GitHub, etc., for a thorough understanding of the individual’s profile, please list links like github and linkedin.{job_description}\n{resume_text}",
                max_tokens=500,
            )

            summary = response.choices[0].text.strip()
            request.summary = copy.deepcopy(summary)

            git_repo_summary = extract_links(request, summary)

            git_repo_summary_json = json.dumps(git_repo_summary, indent=4)


            resume_summary = request.summary

            response2 = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"\n Analyzing a candidate's suitability for a specific role requires a comprehensive evaluation of both their GitHub profile JSON, denoted as {git_repo_summary_json}, and their resume summary, represented as {resume_summary}. By juxtaposing the information extracted from these two sources and aligning them with the specified {job_description}, the goal is to furnish recruiters with customized insights. These insights aim to discern the candidate's compatibility with the outlined job requirements, enabling a well-informed assessment of whether the candidate is a suitable fit for the role or not.",
                max_tokens=350,
            )

            ai_summary = response2.choices[0].text.strip()

            return render(request, 'summary.html', {'ai_summary': ai_summary})
    
    return render(request, 'upload_pdf.html', {'form': form})
