# auto-citrix 🤖
Quick script to automatically login to your citrix VM in the morning

### 🛑 Don't forget to add a config.json file with this format:

    {
        "user": "",
        "password": "",
        "citrix_url": "",
        "auto_sms": true|false,
        "sheet_name": ""
    }

The **auto_sms** flag is a boolean that specifies whether you automated the 2FA SMS needed for the login. If you wish to type it manually into the terminal, you can leave it as false and the sheet_name key will be irrelevant in this case.

## ⭕ Steps to automate the 2FA SMS

- First thing is to download the SMS hooks APK from [this repository](https://github.com/sa3dany/android-sms-hooks/releases) which will send POST requests to a chosen URL by you whenever you receive a message.

- Next thing you'll need is to create a google sheet and activate the correspending API to receive a service account *credentials.json* which you'll have to put in the top level directory of this project.

- Then add the following Apps Script code to your google sheet by clicking on the Extensions tab:

```javascript
    function doPost(e) {
        const two_factor_authentification_provider = "" // 🚨 Don't forget to fill in this variable
        let sms = JSON.parse(e.postData.contents);
        let sheet = SpreadsheetApp.getActive().getSheets()[0];
        if(sms.from == two_factor_authentification_provider){
            sheet.appendRow([sms.timestamp, sms.from, sms.body.split("\n")[0], "No"]);
        }
        return ContentService
            .createTextOutput(JSON.stringify({}))
            .setMimeType(ContentService.MimeType.JSON);
        }
```

- After that, put the generated URL of the Apps Script deployment in the SMS hooks app so that it can send SMS messages directly to the google sheet.

- Finally, you have to add the name of the sheet you created to the config.json

*PS: Don't forget to set the auto_sms key in the config.json to true*