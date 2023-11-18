import json
import requests

class GitHub:
    def __init__(self, link):
        self.link = link
        self.name = 'Github'
        self.result = {}

    def clean(self):
        primary_link = self.link.strip()  # Strip leading/trailing whitespaces
        if primary_link.endswith('/'):
            primary_link = primary_link[:-1]  # Remove trailing slash if present
        self.link = primary_link  # Update the instance variable with the cleaned link

    def api(self):
        # Retrieve the username from the GitHub link
        username = self.link.split('/')[-1]
        
        print(f"GitHub User ID: {username}")

        # Make an API request to fetch the user's repositories
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repos = response.json()

            total_repos = len(repos)
            if total_repos == 0:
                print("No repositories found for the user.")
                return

            total_stars = sum(repo['stargazers_count'] for repo in repos)
            average_stars = total_stars / total_repos

            activity_score = sum(1 for repo in repos if repo['pushed_at']) / total_repos
            popularity_score = sum(1 for repo in repos if repo['stargazers_count'] >= 100) / total_repos
            quality_score = sum(1 for repo in repos if repo['size'] >= 100 and repo['language'] != 'Jupyter Notebook') / total_repos
            open_source_score = sum(1 for repo in repos if repo['forks_count'] > 0) / total_repos
            complexity_score = sum(1 for repo in repos if repo['size'] >= 1000) / total_repos

            pr_response = requests.get(f"https://api.github.com/users/{username}/received_events/public")
            if pr_response.status_code == 200:
                pr_events = pr_response.json()
                collaboration_score = sum(1 for event in pr_events if event['type'] == 'PullRequestEvent') / total_repos
            else:
                collaboration_score = 0

            learning_score = sum(1 for repo in repos if repo['forks_count'] > 0 and repo['language'] == 'Documentation') / total_repos

            # Calculate the overall proficiency score
            proficiency_score = (activity_score + popularity_score + quality_score +
                                 open_source_score + complexity_score +
                                 collaboration_score + learning_score) / 7
            
            # Print a table listing all repositories along with language and star count
            print("\nRepository Table:")
            print("{:<40} {:<20} {:<10}".format("Repository Name", "Language", "Stars"))
            print("-" * 75)
            for repo in repos:
                    repo_name = repo['name']
                    language = repo['language'] if repo['language'] else "Not specified"
                    stars = repo['stargazers_count']
                    print("{:<40} {:<20} {:<10}".format(repo_name, language, stars))
            
            # Print individual scores
            print(f"Activity Score: {activity_score}")
            print(f"Popularity Score: {popularity_score}")
            print(f"Code Quality Score: {quality_score}")
            print(f"Open Source Score: {open_source_score}")
            print(f"Complexity Score: {complexity_score}")
            print(f"Collaboration Score: {collaboration_score}")
            print(f"Learning and Growth Score: {learning_score}")

            # Print overall proficiency score
            print(f"Overall Proficiency Score: {proficiency_score}")

            # Perform keyword analysis
            self.keyword_analysis(repos)

            # Perform benchmarking
            self.benchmarking(proficiency_score)

            # Perform summarization
            self.summarize(proficiency_score)

        else:
            print("Unable to retrieve user repositories.")

    def keyword_analysis(self, repos):
        # Specify the keywords to analyze
        keywords = ['html', 'web development', 'react']

        print("\nKeyword Analysis:")
        for keyword in keywords:
            keyword_count = sum(1 for repo in repos if keyword.lower() in repo['name'].lower())
            print(f"{keyword.capitalize()}: {keyword_count}")

    def benchmarking(self, proficiency_score):
        # Define the benchmark scores
        benchmark_scores = {
            'Fresher': 0.2,
            'Junior Developer': 0.5,
            'Mid-level Developer': 0.7,
            'Senior Developer': 0.9
        }

        print("\nBenchmarking:")
        for role, score in benchmark_scores.items():
            if proficiency_score >= score:
                print(f"Proficiency Level: {role}")
                break

        result_dict = {
            "GitHubUserID": "{username}",
            "RepositoryTable": [{"RepositoryName": repo['name'], "Language": repo['language'], "Stars": repo['stargazers_count']} for repo in "{repos}"],
            "Scores": {
                "ActivityScore: {activity_score}",
                "PopularityScore: {popularity_score}",
                "CodeQualityScore: {quality_score}",
                "OpenSourceScore: {open_source_score}",
                "ComplexityScore: {complexity_score}",
                "CollaborationScore: {collaboration_score}",
                "LearningScore: {learning_score}",
                "OverallProficiencyScore: {proficiency_score}"
            },
            "KeywordAnalysis": {keyword.capitalize(): sum(1 for repo in "{repos}" if keyword.lower() in repo['name'].lower()) for keyword in ['html', 'web development', 'react']},
            "Benchmarking": next((role for role, score in benchmark_scores.items() if proficiency_score >= score), None),
            "Summary": self.get_summary(proficiency_score)
        }

        # Save the result dictionary to a JSON file
        json_filename = "github_analysis_result.json"
        with open(json_filename, 'w') as json_file:
            json.dump(result_dict, json_file, indent=4)

        print(f"Analysis result saved to {json_filename}")

    def get_summary(self, proficiency_score):
        if proficiency_score >= 0.7:
            return "The candidate has a strong profile. Their activity, popularity, code quality, and collaboration scores are high, indicating a well-rounded profile. The candidate's repositories demonstrate a good balance of open source contributions and personal projects."
        elif proficiency_score >= 0.5:
            return "The candidate has a moderate profile. Their activity, popularity, and code quality scores are decent, but there is room for improvement. While they have some open source contributions, more personal projects could be beneficial."
        else:
            return "The candidate has a relatively low profile. Their activity, popularity, code quality, and collaboration scores could be improved. Encouraging the candidate to engage more in open source projects and personal development can enhance their GitHub profile."
