from django import forms

def file_extension_validator(value):
    if not value.name.endswith('.pdf'):
        raise forms.ValidationError('Only PDF files are allowed.')

class ResumeUploadForm(forms.Form):
    resume_pdf = forms.FileField(label='Select a PDF file', validators=[file_extension_validator])
    job_description = forms.CharField(label='Enter job description', widget=forms.Textarea)


