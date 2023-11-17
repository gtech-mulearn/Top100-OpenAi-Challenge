import re
from django.shortcuts import render
from django.http import JsonResponse
import openai
import fitz
from .forms import ResumeUploadForm
from .main import PdfParser
from .github import GitHub 
import copy
import os

def extract_links(request,text):
    # Use a regular expression to find URLs in the text
    summarized_resume=copy.deepcopy(text)
    url_pattern = re.compile(r'https?://github\S+')
    links = re.findall(url_pattern, text) 
    print(links)
    if len(links)>1:
        github=GitHub(links[0])
    else:
        return None
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=generate_resume_summarization_task(summarized_resume),
                max_tokens=500,
            )
        ai_summary = response.choices[0].text.strip()
        # return JsonResponse({'task_generated': task_generated})
        return render(request, 'summary.html', {'ai_summary': ai_summary})
    print("result:",github.results)
    return github.results

def generate_resume_summarization_task(resume_summary):
    """
    Generate a resume summarization machine task for testing candidate capabilities.

    Args:
    - resume summarized summary
    Returns:
    - str: The generated task with placeholders.
    """

    task_template = f"""
    **Task: Machine Test**

    ---

    **Description:**

    Recruiters often need to give some task to verify candidate knowledge

    **Input:**

    Provide a resume summary generated using openai.

    **Output:**

    The system should generate task according to candidate skills:

    

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
            # Get the uploaded resume PDF file
            resume_pdf = form.cleaned_data['resume_pdf']
            

            # Read the resume PDF and extract text
            doc = fitz.open(resume_pdf)
            resume_text = ""
            for page in doc.pages():
                resume_text += page.get_text()

            job_description = form.cleaned_data['job_description']

            # Call OpenAI API for summarization
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"\n Conduct a comprehensive analysis of the individual’s profile, taking into account all the information provided. This should include an evaluation of their educational background, work history, skills, and notable achievements. Be sure to also examine any links included in the resume for additional information, especially those leading to professional networking sites like LinkedIn, or repositories showcasing their work, such as GitHub. Identify any potential areas of concern or exceptional strengths. Consider their career progression and how their experiences align with their goals. Also, assess their potential for growth and adaptability in various contexts. Remember to scrape all the links in the resume, particularly those to LinkedIn, GitHub, etc., for a thorough understanding of the individual’s profile,please list links like github and linkedin.{job_description}\n{resume_text}",
                max_tokens=500,
            )

            # Extract the summary from OpenAI's response
            summary = response.choices[0].text.strip()
            request.summary = copy.deepcopy(summary)

            git_repo_summary = extract_links(request,summary)

            resume_summary=request.summary
     

            # Make an API call to OpenAI GPT-3
            response2 = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"\n Given a candidate's GitHub profile JSON data and summarized resume, compare the two sources and provide tailored insights for recruiters. Highlight any discrepancies, showcase complementary information,and offer insights that recruiters can leverage to make informed decisions. Consider factors such as the candidate's skills, academic background, versatility, achievements, GitHub activity, and any potential for growth. Ensure the insights are presented in a way that facilitates recruiters in assessing the candidate's overall suitability for the position{resume_summary}\n{git_repo_summary} ",
                max_tokens=200,  # Adjust max_tokens as needed
            )

            # Extract the overall summary from the response
            ai_summary = response2.choices[0].text.strip()

            # request.summary = summary
            # return render(request,'summary.html', {"ai_summary",ai_summary})
            # return JsonResponse({'summary': ai_summary})
            return render(request, 'summary.html', {'ai_summary': ai_summary})
git 
    return render(request, 'upload_pdf.html', {'form': form})
