import time
import xbmc
import os
import xbmcgui
import urllib2
import webbrowser

site1qr = xbmc.translatePath('special://home/addons/script.cerebro.pairwith/site1.png')
site2qr = xbmc.translatePath('special://home/addons/script.cerebro.pairwith/site2.png')
site3qr = xbmc.translatePath('special://home/addons/script.cerebro.pairwith/site3.png')
site4qr = xbmc.translatePath('special://home/addons/script.cerebro.pairwith/site4.png')
site5qr = xbmc.translatePath('special://home/addons/script.cerebro.pairwith/site5.png')

def menuoptions():
    dialog = xbmcgui.Dialog()
    funcs = (
        function1,
        function2,
        function3,
        function4
        )
        
    call = dialog.select('[B][COLOR=yellow]EyePeaTV[/COLOR][COLOR=red] Pair-ing System[/COLOR][/B]', [
    '[B][COLOR=white]      Open Load[/COLOR][/B] [COLOR=red]Website[/COLOR]', 
    '[B][COLOR=white]      The Video Me[/COLOR][/B] [COLOR=red]Website[/COLOR]',
    '[B][COLOR=white]      Vid Up Me[/COLOR][/B] [COLOR=red]Website[/COLOR]',
	'[B][COLOR=white]      FlashX[/COLOR][/B] [COLOR=red]Website[/COLOR]'
	])
    # dialog.selectreturns
    #   0 -> escape pressed
    #   1 -> first item
    #   2 -> second item
    if call:
        # esc is not pressed
        if call < 0:
            return
        func = funcs[call-4]
        return func()
    else:
        func = funcs[call]
        return func()
    return 

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

myplatform = platform()
    
def function1():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vistatv.online/p/?site=1' ) )
    else:
        opensite = webbrowser . open('http://vistatv.online/p/?site=1')

def function2():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vistatv.online/p/?site=2' ) )
    else:
        opensite = webbrowser . open('http://vistatv.online/p/?site=2')
        
def function3():
    if myplatform == 'android': # Android 
       opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vistatv.online/p/?site=3' ) )
    else:
        opensite = webbrowser . open('http://vistatv.online/p/?site=3')
       
		
def function4():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vistatv.online/p/?site=5' ) )
    else:
        opensite = webbrowser . open('http://vistatv.online/p/?site=5') # NOW NUMBER 4
     
menuoptions()
