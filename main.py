from flask import Flask, jsonify, request, render_template
import openai
import concurrent.futures
from utils import auth_required

app = Flask(__name__)
# Set your OpenAI API key here
openai.api_key = "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"

# Custom error handlers
@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error="Bad Request"), 400


@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', error="Unauthorized"), 401


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Not Found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error="Internal Server Error"), 500


@app.route('/')
def home():
    return "<h1>Home!</h1>"


def rephrase_prompt(text, num_values):
    rephrased_texts = []

    def rephrase_single(prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=len(text) + 100,
            temperature=0.7,
            top_p=0.98,
            frequency_penalty=0.2,
            presence_penalty=0.5,
            stop="###STOP###",
        )
        return response.choices[0].text.strip()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        prompts = [f"Rephrase the following sentence: '{text}'" for _ in range(num_values)]
        rephrased_responses = list(executor.map(rephrase_single, prompts))

    return rephrased_responses


@app.route('/rephraser', methods=['GET', 'POST'])
@auth_required
def rephraser():
    print("Hello 1")
    if request.method == 'POST':
        print("Hello 2")
        description = request.form.get('description')
        print("Hello 3")
        num_values = int(request.form.get('num_values'))
        print("Sentence:", description)
        print("Number of Iterations:", num_values)
        rephrased_responses = rephrase_prompt(description, num_values=num_values)
        return render_template('result.html', rephrased_responses=rephrased_responses)

    return render_template('index.html')


@app.route('/content_generation', methods=['GET', 'POST'])
@auth_required
def content_generation():
    if request.method == 'POST':
        # Process form data and generate sections
        description = request.form.get('description')
        section_names = request.form.getlist('section_name[]')
        titles = request.form.getlist('title[]')
        descriptions = request.form.getlist('description[]')

        # Process other input fields and generate sections...
        sections = {}
        for i, section_name in enumerate(section_names):
            sections[section_name] = {
                "title": titles[i],
                "description": descriptions[i]
            }

        # Render the result page with the generated sections
        return render_template('content_generation_result.html', generated_sections=sections)

    return render_template('content_generation.html')  # Display the input form for GET requests


def generate_section_content(business_description, section_name):
    prompt = f"Generate content for the '{section_name}' section of our website based on the following business description:\n\n{business_description}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,  # Adjust the length of the generated content
        temperature=0.7,
        top_p=0.98,
        frequency_penalty=0.2,
        presence_penalty=0.5,
        stop=None,
    )

    section_content = response.choices[0].text.strip()

    return section_content


# Your generate_section_content function here...

@app.route('/content_generator', methods=['GET', 'POST'])
def content_generator():
    if request.method == 'POST':
        # Process form data and get field values
        about_title = request.form.get('about_title')
        about_description = request.form.get('about_description')
        refunds_title = request.form.get('refunds_title')
        refunds_description = request.form.get('refunds_description')
        hero_title = request.form.get('hero_title')
        hero_subtitle = request.form.get('hero_subtitle')

        sections = []

        if about_title and about_description:
            sections.append(("About", about_title, about_description))
        if refunds_title and refunds_description:
            sections.append(("Refunds", refunds_title, refunds_description))
        if hero_title and hero_subtitle:
            sections.append(("Hero", hero_title, hero_subtitle))
        # Add more sections here...

        generated_sections = []

        for section_name, title, description in sections:
            section_content = generate_section_content(description, section_name)
            generated_sections.append((section_name, title, description, section_content))

        return render_template('content_generation_result.html', generated_sections=generated_sections)

    return render_template('content_generation.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)