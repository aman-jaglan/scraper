import openai

openai.api_key = "YOUR_API_KEY"

def customize_resume(resume_text, job_description):
    prompt = f"Your task is to tailor the resume for the job described below.\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nExtract the key skills and requirements from the job description and ensure the resume highlights those skills. Provide a revised resume summary that aligns with the job requirements."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    # Extract the assistant's reply
    tailored_summary = response['choices'][0]['message']['content']
    return tailored_summary
