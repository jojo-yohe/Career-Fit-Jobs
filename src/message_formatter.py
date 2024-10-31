from telegraph import Telegraph
from config import JOB_CATEGORIES
from datetime import datetime

def create_job_update(matched_jobs):
    telegraph = Telegraph()
    telegraph.create_account(short_name='CareerFitJobs')

    content = '<b>📋 Latest Job Listings</b>'
    
    for category, jobs in matched_jobs.items():
        content += f'<h4>🔹 {category}</h4>'
        for job in jobs:
            job_title = job['summary'].split('\n')[0][:50]  # Get first line, up to 50 chars
            content += f'''
            <p>
            📢 <b>{job['channel']}</b><br>
            💼 <code>{job_title}</code><br>
            🔗 <a href="{job['message_link']}">View full job details</a>
            </p>
            <hr>
            '''

    current_date = datetime.now().strftime("%Y-%m-%d")
    page_title = f'Career Fit Jobs - {current_date}'
    
    response = telegraph.create_page(
        page_title,
        html_content=content,
        author_name='Career Fit Jobs Bot'
    )
    return response['url']

def create_promotion_banner():
    telegraph = Telegraph()
    telegraph.create_account(short_name='CareerFitJobsPromo')

    content = '''
    <h3>Upgrade Your Job Search with Career Fit Jobs!</h3>
    <p>Get personalized job listings delivered right to your Telegram:</p>
    <ul>
        <li>Tailored job recommendations based on your preferences</li>
        <li>Daily updates from top companies</li>
        <li>Easy application process directly through Telegram</li>
    </ul>
    <p><b><a href="https://t.me/CareerFitJobsBot">Start Your Upgraded Job Search Now!</a></b></p>
    '''

    response = telegraph.create_page(
        'Career Fit Jobs - Upgrade Your Job Search',
        html_content=content,
        author_name='Career Fit Jobs Bot'
    )
    return response['url']
