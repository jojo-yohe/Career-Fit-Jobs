from telegraph import Telegraph
from config import JOB_CATEGORIES
from datetime import datetime

def create_job_update(matched_jobs):
    telegraph = Telegraph()
    telegraph.create_account(short_name='CareerFitJobs')

    # Improved HTML structure for better instant view
    content = '''
    <article>
        <h3>📋 Latest Job Listings</h3>
        <div class="job-listings">
    '''
    
    for category, jobs in matched_jobs.items():
        content += f'<h4>🔹 {category}</h4><div class="category-jobs">'
        for job in jobs:
            title = job['summary'].split('\n')[0][:100]
            content += f'''
                <div class="job-card">
                    📢<h5>{job['channel']}</h5>
                    💼<p>{title}</p>
                    <a href="{job['message_link']}">View full job details</a>
                </div>
            '''
        content += '</div>'
    
    content += '</div></article>'

    current_date = datetime.now().strftime("%Y-%m-%d")
    response = telegraph.create_page(
        title=f'Career Fit Jobs - {current_date}',
        html_content=content,
        author_name='Career Fit Jobs Bot',
        author_url='https://t.me/CareerFitJobsBot'
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
