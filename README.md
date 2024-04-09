# CodeGuardian: The AI Sentinel for GitLab Reviews

## Overview

CodeGuardian leverages the power of AI to automate code reviews within GitLab, aiming to enhance code quality, enforce coding standards, and streamline the development workflow. By integrating directly with GitLab via webhooks, CodeGuardian provides immediate, insightful feedback on merge requests, focusing primarily on Python projects. This feedback includes analysis on code quality, style compliance, potential bugs, and performance optimizations.

## Features

- **Automated Code Reviews**: Instant feedback on merge requests to improve code quality.
- **Python Support**: Specialized in reviewing Python code, with plans to support more languages in the future.
- **Integration with GitLab**: Uses GitLab webhooks to trigger code reviews on new or updated merge requests.
- **AI-Powered Insights**: Utilizes the `codellama` AI model for deep code analysis and actionable recommendations.
- **Customizable Review Rules**: Offers the ability to define project-specific review guidelines and standards.

## Getting Started

### Prerequisites

- GitLab account and repository.
- Access to the `codellama` API.
- Python development environment for running the webhook receiver service.

### Setup

1. **Configure GitLab Webhook**:
   - Navigate to your GitLab project's Settings > Webhooks page.
   - Enter the URL of your deployed CodeGuardian service as the webhook endpoint.
   - Select "Merge Request events" and save.

2. **Deploy CodeGuardian Service**:
   - Ensure your server or cloud function is set up to receive webhook events from GitLab.
   - Deploy the CodeGuardian service, making sure it's accessible by GitLab.

3. **`codellama` API Configuration**:
   - Obtain your `codellama` API key and configure it within the CodeGuardian service for authentication.

### Usage

Once set up, CodeGuardian automatically reviews any new or updated merge requests in your GitLab project. Review feedback will be posted as comments directly on the merge requests, providing valuable insights and suggestions for improvements.

## Contributing

We welcome contributions to CodeGuardian! Whether you're looking to add support for new languages, improve the integration, or suggest new features, please feel free to fork the repository, make your changes, and submit a pull request.

## License

[MIT License](LICENSE.md) - see the LICENSE file for details.

## Acknowledgments

- The `codellama` team for providing the AI model that powers our code reviews.
- The GitLab team for their robust platform and webhook functionality.
