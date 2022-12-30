import os
import subprocess



right_result_1 = """{
  "glossary": {
    "GlossDiv": {
      "GlossList": {
        "GlossEntry": {
          "Abbrev": "ISO 8879:1986",
          "Acronym": "SGML",
          "GlossDef": {
            "GlossSeeAlso": "GML",
            "para": "A meta-markup language, used to create markup languages such as DocBook."
          },
          "GlossSee": "markup",
          "GlossTerm": "Standard Generalized Markup Language",
          "ID": "SGML",
          "SortAs": "SGML"
        }
      },
      "title": "S"
    },
    "title": "example glossary"
  }
}"""

right_result_2 = """{
  "a": [
    {
      "b": 1.000000
    }
  ]
}"""

right_result_3 = """Expected JSON input argument to parse"""

right_result_4 = """{
  "web-app": {
    "servlet": [
      {
        "init-param": {
          "cachePackageTagsRefresh": 60.000000,
          "cachePackageTagsStore": 200.000000,
          "cachePackageTagsTrack": 200.000000,
          "cachePagesDirtyRead": 10.000000,
          "cachePagesRefresh": 10.000000,
          "cachePagesStore": 100.000000,
          "cachePagesTrack": 200.000000,
          "cacheTemplatesRefresh": 15.000000,
          "cacheTemplatesStore": 50.000000,
          "cacheTemplatesTrack": 100.000000,
          "configGlossary:adminEmail": "ksm@pobox.com",
          "configGlossary:installationAt": "Philadelphia, PA",
          "configGlossary:poweredBy": "Cofax",
          "configGlossary:poweredByIcon": "/images/cofax.gif",
          "configGlossary:staticPath": "/content/static",
          "dataStoreClass": "org.cofax.SqlDataStore",
          "dataStoreConnUsageLimit": 100.000000,
          "dataStoreDriver": "com.microsoft.jdbc.sqlserver.SQLServerDriver",
          "dataStoreInitConns": 10.000000,
          "dataStoreLogFile": "/usr/local/tomcat/logs/datastore.log",
          "dataStoreLogLevel": "debug",
          "dataStoreMaxConns": 100.000000,
          "dataStoreName": "cofax",
          "dataStorePassword": "dataStoreTestQuery",
          "dataStoreTestQuery": "SET NOCOUNT ON;select test='test';",
          "dataStoreUrl": "jdbc:microsoft:sqlserver://LOCALHOST:1433;DatabaseName=goon",
          "dataStoreUser": "sa",
          "defaultFileTemplate": "articleTemplate.htm",
          "defaultListTemplate": "listTemplate.htm",
          "jspFileTemplate": "articleTemplate.jsp",
          "jspListTemplate": "listTemplate.jsp",
          "maxUrlLength": 500.000000,
          "redirectionClass": "org.cofax.SqlRedirection",
          "searchEngineFileTemplate": "forSearchEngines.htm",
          "searchEngineListTemplate": "forSearchEnginesList.htm",
          "searchEngineRobotsDb": "WEB-INF/robots.db",
          "templateLoaderClass": "org.cofax.FilesTemplateLoader",
          "templateOverridePath": "",
          "templatePath": "templates",
          "templateProcessorClass": "org.cofax.WysiwygTemplate",
          "useDataStore": true,
          "useJSP": false
        },
        "servlet-class": "org.cofax.cds.CDSServlet",
        "servlet-name": "cofaxCDS"
      },
      {
        "init-param": {
          "mailHost": "mail1",
          "mailHostOverride": "mail2"
        },
        "servlet-class": "org.cofax.cds.EmailServlet",
        "servlet-name": "cofaxEmail"
      },
      {
        "servlet-class": "org.cofax.cds.AdminServlet",
        "servlet-name": "cofaxAdmin"
      },
      {
        "servlet-class": "org.cofax.cds.FileServlet",
        "servlet-name": "fileServlet"
      },
      {
        "init-param": {
          "adminGroupID": 4.000000,
          "betaServer": true,
          "dataLog": 1.000000,
          "dataLogLocation": "/usr/local/tomcat/logs/dataLog.log",
          "dataLogMaxSize": "",
          "fileTransferFolder": "/usr/local/tomcat/webapps/content/fileTransferFolder",
          "log": 1.000000,
          "logLocation": "/usr/local/tomcat/logs/CofaxTools.log",
          "logMaxSize": "",
          "lookInContext": 1.000000,
          "removePageCache": "/content/admin/remove?cache=pages&id=",
          "removeTemplateCache": "/content/admin/remove?cache=templates&id=",
          "templatePath": "toolstemplates/"
        },
        "servlet-class": "org.cofax.cms.CofaxToolsServlet",
        "servlet-name": "cofaxTools"
      }
    ],
    "servlet-mapping": {
      "cofaxAdmin": "/admin/*",
      "cofaxCDS": "/",
      "cofaxEmail": "/cofaxutil/aemail/*",
      "cofaxTools": "/tools/*",
      "fileServlet": "/static/*"
    },
    "taglib": {
      "taglib-location": "/WEB-INF/tlds/cofax.tld",
      "taglib-uri": "cofax.tld"
    }
  }
}"""


right_result_5 = """{
  "glossary": {
    "GlossDiv": {
      "GlossList": {
        "GlossEntry": {
          "Abbrev": "ISO 8879:1986",
          "Acronym": "SGML",
          "GlossDef": {
            "GlossSeeAlso": "GML",
            "para": false
          },
          "GlossSee": "markup",
          "GlossTerm": "Standard Generalized Markup Language",
          "ID": "SGML",
          "SortAs": "SGML"
        }
      },
      "title": "S"
    },
    "title": "example glossary"
  }
}"""


def system_run_command(command, ignore_stderr=True, additional_env=dict()):
    cmd_env = os.environ.copy()
    cmd_env.update(additional_env)
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=cmd_env,
    )

    output, errors = p.communicate()
    if p.returncode or (not ignore_stderr and errors):
        return errors.decode("utf-8").strip()

    p.wait()
    result = output.decode("utf-8").strip()
    return result


if __name__ == "__main__":

    result_1 = system_run_command("./build/parse_json \"$(cat ./data/glossary.json)\"")
    assert result_1 == right_result_1, f"\nTEST_1 FAULT\nright: {right_result_1.split()}\ngiven: {result_1.split()}"

    result_2 = system_run_command("./build/parse_json \"$(cat ./data/object_in_array.json)\"")
    assert result_2 == right_result_2, f"\nTEST_2 FAULT\nright: {right_result_2.split()}\ngiven: {result_2.split()}"

    result_3 = system_run_command("./build/parse_json", ignore_stderr=False)
    assert result_3 == right_result_3, f"\nTEST_3 FAULT\nright: {right_result_3.split()}\ngiven: {result_3.split()}"

    result_4 = system_run_command("./build/parse_json \"$(cat ./data/cofax.json)\"")
    assert result_4 == right_result_4, f"\nTEST_4 FAULT\nright: {right_result_4.split()}\ngiven: {result_4.split()}"

    result_5 = system_run_command("./build/parse_json \"$(cat ./data/test.json)\"")
    assert result_5 == right_result_5, f"\nTEST_5 FAULT\nright: {right_result_5.split()}\ngiven: {result_5.split()}"
