from telegraph import Telegraph

def get_privacy_policy_url():
    telegraph = Telegraph()
    telegraph.create_account(short_name='JobSearchBot')

    content = '''
    <h3>Privacy Policy for Career Fit Job Bot</h3>
    <p>Last updated: [Current Date]</p>
    
    <h4>1. Information We Collect</h4>
    <p>We collect your Telegram user ID and job preferences to provide personalized job updates.</p>
    
    <h4>2. How We Use Your Information</h4>
    <p>We use your information to send relevant job listings based on your preferences.</p>
    
    <h4>3. Data Storage and Security</h4>
    <p>Your data is securely stored in our database and is not shared with third parties.</p>
    
    <h4>4. Your Rights</h4>
    <p>You can update or delete your preferences at any time using bot commands.</p>
    
    <h4>5. Changes to This Policy</h4>
    <p>We may update this policy. Please check periodically for any changes.</p>
    
    <h4>6. Contact Us</h4>
    <p>If you have any questions, please contact [Your Contact Info].</p>
    '''

    response = telegraph.create_page(
        'Career Fit Job Bot - Privacy Policy',
        html_content=content
    )
    return response['url']

if __name__ == '__main__':
    print(get_privacy_policy_url())
