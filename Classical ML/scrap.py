import openai
import json
import time

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = "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"

# List of university website links to scrape
university_links = [
    "https://www.torrens.edu.au/courses",
    "https://federation.edu.au/",
    "https://www.utas.edu.au/",
    "https://www.westernsydney.edu.au/"
]


def scrape_course_info(website_link):
    # Dynamic prompt generation based on the website link
    prompt = f"Scrape course information from {website_link}."

    try:
        # Call the OpenAI API to retrieve structured data in JSON format
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the GPT-3.5 engine
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7,
            n=1,
            stop=None,
            timeout=60,
        )

        # Check if the API response is empty or not
        if 'choices' in response and len(response['choices']) > 0:
            course_info_json = response['choices'][0]['text']
            return course_info_json
        else:
            print(f"Empty response for {website_link}")
            return None

    except Exception as e:
        print(f"Error scraping {website_link}: {str(e)}")
        return None


def main():
    course_info_by_university = {}

    for university_link in university_links:
        course_info_json = scrape_course_info(university_link)

        if course_info_json:
            try:
                university_name = university_link.split("//")[-1].split(".")[1]
                course_info = json.loads(course_info_json)

                # Save the scraped data in JSON format for each university
                file_name = f"{university_name}_course_info.json"
                with open(file_name, 'w') as json_file:
                    json.dump(course_info, json_file, indent=4)

            except Exception as e:
                print(f"Error parsing JSON for {university_link}: {str(e)}")

        # Introduce a delay between API requests to avoid rate-limiting issues
        time.sleep(20)


if __name__ == "__main__":
    main()
