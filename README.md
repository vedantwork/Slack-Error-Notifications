# Slack Error Notifications

The Slack Error Notifications feature provides real-time alerts for errors occurring within your application. By integrating Slack with your error monitoring system, you can ensure that critical issues are promptly communicated to your development and operations teams, enabling swift action.

## Useful Links

- 📕 [Slack API Website](https://api.slack.com/)
- 📗 [Slack Website](https://slack.com/intl/en-ca/)

## Setting Up Slack Notifications

Follow these steps to set up Slack notifications for your application:

### 1. Create a New Slack Workspace
   - Visit the [Slack Website](https://slack.com/intl/en-ca/) and create a new workspace.
   - Click on `Create a Workspace`.
   - Enter the name of your workspace (e.g., `Error Notification`).
   - Skip the step to invite team members if you prefer.

   <img src="Reference Snaps/Screenshot_1.png">
   <img src="Reference Snaps/Screenshot_2.png">
   <img src="Reference Snaps/Screenshot_3.png">
   <img src="Reference Snaps/Screenshot_4.png">
   <img src="Reference Snaps/Screenshot_5.png">

### 2. Create a Slack App
   -Visit the [Slack API Website](https://api.slack.com/) for more details on creating and managing Slack apps.
   - To send notifications to your Slack channel, you need to create an app.
   - Click on `Create an App`.
   - Select your workspace in the "Pick a workspace to develop your app" section and click on `Create App`.

  <img src="Reference Snaps/Screenshot_6.png">
  <img src="Reference Snaps/Screenshot_7.png">

### 3. Configure App Scopes
   - Under `Features`, navigate to `App Home` and click on `Review Scopes to Add`.
   - Click on `Add an OAuth Scope`.
   - Search for `chat:write` and add it to your app.

  <img src="Reference Snaps/Screenshot_8.png">
  <img src="Reference Snaps/Screenshot_9.png">
  <img src="Reference Snaps/Screenshot_10.png">

### 4. Generate and Use the OAuth Token
   - Go to the `OAuth & Permissions` tab.
   - Generate an OAuth Token and copy it.
   - Paste the token into your `.env` file for secure usage.

   <img src="Reference Snaps/Screenshot_11.png">

### 5. Integrate the App with Your Slack Channel
   - In Slack, click on the channel where you want to send notifications.
   - Go to `Integrations` and click on `Add an App`.
   - Select the app you created and click on `Add`.

  <img src="Reference Snaps/Screenshot_12.png">
  <img src="Reference Snaps/Screenshot_13.png">
  <img src="Reference Snaps/Screenshot_14.png">

### 6. Start Sending Notifications
   - Now that everything is set up, you can start sending notifications to your Slack channel.

  <img src="Reference Snaps/Screenshot_15.png">

 Volla! You have successfully set up Slack Error Notifications for your application.
