# clova-apitore-tweet_summary
This is an example project.

This skill informs the latest trend tweet about the terms you specify. Skill response will be forwarded to your LINE notify.

## Requirements
- Python 3.6
- LINE Clova
  - [ ] Activate skill store (in Clova apps)
  - [ ] Create [your own skill](https://clova-developers.line.me/)
- LINE Notify
  - [ ] Obtain [notify token](https://notify-bot.line.me/my/)
- Apitore
  - [ ] Create [Apitore account](https://apitore.com/store/index.html)
  - [ ] Register [TweetSummary API](https://apitore.com/store/apis/details?id=27)
  - [ ] Activate [Twitter account link](https://apitore.com/me/top)
  - [ ] Obtain [Apitore access token](https://apitore.com/me/apis/registered)
  
## Set your tokens
Set your `Extension ID`, `LINE notify token` and `Apitore access token`.

```python
application_id = "YOUR EXTENSION ID"
clova = Clova(application_id=application_id, default_language="ja", debug_mode=True)

line_notify_token = 'YOUR LINE NOTIFY TOKEN'
line_notify_api = 'https://notify-api.line.me/api/notify'

apitore_access_token = 'YOUR APITORE ACCESS TOKEN'
apitore_tweet_summarize_api = 'https://api.apitore.com/api/27/twitter-summarize/get'
```
