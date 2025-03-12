# Session 06 worklog

## 1) Add Monitoring to Your Systems
We use Grafana to create real-time dashboards that provide a visual representation of our system's metrics, making it easier to monitor and identify potential issues.

Our Grafana dashboard is accessible at http://146.190.207.33:3000/, where you can view various metrics such as CPU and memory usage, network traffic, and response times. By monitoring these metrics, we can quickly identify and respond to any performance or availability issues before they impact our users.

## 2) Software Maintenance
At the current time, there are no issuse present in our system based on the dashboard provided by Helge and the TA's.

Group a, dashboard: http://104.248.134.203/status.html

Our Grafana dashboard can be found: http://146.190.207.33:3000

## 3) Software Maintenance II
We group a Academic Weapons -[checks]-> Group b DevUps: Delivering Buggy Software Late since 2023.

We've created 3 issues on group B's github, concernning the issues we found while testing their Minitwit. A big issue is, no twits are shown, when we access the site. It appears the website is loading all twits, and therefore works until the browser eventually suggests closing the webpage, or the webpage itself just freeze and completely ceases all functionality. 

It's possible to sign-up, however, on success you're redirected to a 404 page. You can return to the main page, and press login before the frontpage freezes, and you'll actually be logged in. This will show a box wherein you're able to write a twit, with other twits possibly being shown below. However, this also struggles with the same issue as first mentioned, and it will eventually freeze / never show any twits.

Lastly &mdash; a bit nickpicky &mdash; but attempting to sign-up with a taken username, results in a nice pop-up that simply displays the message "an error occurred", and it's also possible to sign up with an invalid email address, ie. test@t.

Functionally concerning other users and twits weren't possible to test, as no twits &mdash; and therefore users &mdash; where never shown. 
