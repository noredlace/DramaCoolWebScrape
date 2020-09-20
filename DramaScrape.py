import webbrowser

wb = webbrowser.open("https://www3.dramacool.movie/1-night-2-days-s04-episode-1.html", new=2)
wb.document.getElementsByClassName('cf-download')[0].children[2].getAttribute("href").toString()

#Login to Site To Get Timer to Pick Up After Restart
#$ie = New-Object -ComObject 'internetExplorer.Application'
#$ie.Visible= $true # Make it visible
#
#$ie.Navigate("https://www3.dramacool.movie/1-night-2-days-s04-episode-1.html")
#
#While ($ie.Busy -eq $true) {Start-Sleep -Seconds 3;}
#
#$Link = $ie.document.getElementsByClassName('cf-download')[0].children[2].getAttribute("href").toString()
#$Link.click()
#
#$ie.Quit()

