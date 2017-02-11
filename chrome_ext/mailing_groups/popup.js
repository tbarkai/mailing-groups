var WEBAPP_URL = "http://127.0.0.1:5000/mailinggroups/resolve/";

function loadDoc(emails) {
  if (emails == null) {
    document.body.innerHTML = "This extension only works within a GMail tab!";
    return;
  }
  if (emails[0] == 'EMPTY') {
    document.body.innerHTML = "No recipient emails were detected!"
    return;
  }
  if (emails[0] == 'CLOSED') {
    document.body.innerHTML = "This extension only works while composing a message.";
    return;
  }
  document.getElementById("target").src = WEBAPP_URL + emails.join();
}

document.addEventListener('DOMContentLoaded', function() {
  chrome.tabs.query({active: true}, function(tabs) {
    var tab = tabs[0];
    chrome.tabs.executeScript(tab.id, {
      code: "(function() {\n\
        emailFields = document.querySelectorAll('[aria-label=\"To\"],[aria-label=\"Cc\"],[aria-label=\"Bcc\"]');\n\
        if (emailFields.length == 0) {\n\
          return ['CLOSED'];\n\
        }\n\
        var emails = [];\n\
        for (var i = 0; i < emailFields.length; i++) {\n\
          emailElems = emailFields[i].parentElement.querySelectorAll('[email]');\n\
          for (var x of emailElems) {\n\
            emails.push(x.attributes['email'].textContent);\n\
          }\n\
        }\n\
        if (emails.length == 0) {\n\
          return ['EMPTY'];\
        }\n\
        return emails;\n\
      })()"
    }, loadDoc);
  });
}, false);
