from app.reports.repository_reporter import RepositoryReport

def generate_markdown_report(report: RepositoryReport) -> str:
   if report.total_repositories == 0:
      return f"\n \n # Github Report \n\n No repositories in the list."

   markdown_report = f"\n\n # Github Report\n\n"
   markdown_report += f"================\n\n"
   markdown_report += f"Total Repositories: {report.total_repositories}\n\n"
   for language, count in sorted(report.repositories_by_language.items()):
       markdown_report += f"- {language}: {count}\n"
   markdown_report += f"\n\n Average Stars: {report.average_stars:0f}\n\n"
   markdown_report += f"Most Starred Repository: \n\n"
   if report.most_starred_repository is not None:
      repository = report.most_starred_repository
      markdown_report += f"{repository.owner}/{repository.name} : ({repository.stars}) stars\n\n"

   return markdown_report