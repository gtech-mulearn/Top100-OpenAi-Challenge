# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
import openai
import fitz
from .forms import ResumeUploadForm

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
            openai.api_key = ""
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"\n Conduct a thorough assessment of the candidate's profile by examining their educational background, work history, skills, and noteworthy accomplishments. Evaluate the alignment of their experiences with career goals, considering aspects such as career progression, exceptional strengths, and potential areas of concern. Additionally, provide a summary of the candidate's potential for growth and adaptability in diverse contexts. In the context of a specific job description, rigorously analyze the candidate's suitability for the specified position. Start by assessing if the candidate meets the essential qualifications outlined in the job description. Subsequently, offer a detailed and impartial assessment of their professional background, skills, and experiences, emphasizing relevant achievements. Maintain objectivity, avoiding overemphasis or bias, while presenting an accurate depiction of the candidate's qualifications and potential fit for the role. Highlight key strengths and areas of expertise, giving due consideration to potential gaps or areas for improvement. Furthermore, provide insights into how the candidate could contribute to the organization, ensuring a nuanced and objective evaluation. Additionally, include links to relevant platforms such as GitHub and LinkedIn from the provided resume to facilitate a more in-depth view of their professional portfolio in bulletin format.{job_description}\n{resume_text}",
                max_tokens=500,
            )

            # Extract the summary from OpenAI's response
            summary = response.choices[0].text.strip()
            request.summary = summary

            return JsonResponse({'summary': summary})

    return render(request, 'upload_pdf.html', {'form': form})
