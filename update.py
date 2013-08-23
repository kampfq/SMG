def update():
    try:
        version = urllib2.urlopen('http://league-insanity.tk/Azeirah_content' +
                                  '/version').read()
        global versionNew
        versionNew = version
        # makes sure that the dialog, second window stays open.
        # if it weren't global its variable would be deleted because
        # it went out of scope, bye bye window ;(
        if not float(VERSION) >= float(version):
            try:
                # Gets the current file directory
                cur_dir = os.getcwd()
                # Tempdir /update/ for all the update files.
                update_path = cur_dir + r'\update'

                def downloadUpdate():
                    # This is the actual download
                    response = urllib2.urlopen('https://sourceforge.'
                                               'net/projects/obsmusicstreamd/files/SMG.zip/download')
                    # If /update/ dir exists, do nothing. Else create the dir
                    if not os.path.exists(update_path):
                        os.makedirs(update_path)
                    # Tries to create updated.zip
                    with open(cur_dir + r'\update\updated.zip', 'w+') as updatezip:
                        pass
                    # Writes the downloaded zip to this file
                    with open(cur_dir + r'\update\updated.zip', 'wb') as updatezip:
                        updatezip.write(response.read())
                    # Loads the zip file in a zip object
                    zippy = zipfile.ZipFile(cur_dir + r'\update\updated.zip')
                    if 'gui.exe' in zippy.namelist():
                        downloadUpdate()
                    return zippy

                zippy = downloadUpdate()

                zippy.extractall(path=update_path)

                # Makes sure the file is accessible, otherwise we'd get a
                # WindowsError
                # prevents file being used by another process error (this
                # program)
                del zippy
                os.remove(update_path + r'\updated.zip')

                for fil in os.listdir(cur_dir + r'\\update\\'):
                    print cur_dir + '\\update\\' + fil
                    src = cur_dir + r'\\update\\' + fil
                    dest = cur_dir + '\\' + fil
                    try:
                        os.renames(src, dest)
                    except:
                        pass
                global running
                global success
                success = True
                running = False
                print 'done'

            except IOError as err:
                running = False
                print 'IOError'
                if hasattr(err, 'code'):  # HTTPError
                    print 'first err'
                    logging.exception(err)
                    print 'http error code: ', err.code
                elif hasattr(err, 'reason'):  # URLError
                    print 'sec err'
                    logging.exception(err)
                    update()
                else:
                    print 'lasterr'
                    logging.exception(err)
                    update()

    except IOError as err:
        running = False
        logging.exception(err)
        update()


def updater():
    reply = QMessageBox.question(update_dialog, 'Message', "Do you want " +
                                 "to update?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        update_dialog.show()
        update_dialog_lbl.show()

        Thread(name='Updater', target=update).start()
    else:
        running = False
        sys.exit()

if __name__ == '__main__':
    print 'Before anything'
    from PySide.QtGui import QApplication, QWidget, QLabel, QMessageBox
    print 'from PySide.QtGui import *'
    from threading import Thread
    print 'from threading import Thread'
    from Constants import VERSION
    print 'from Constants import VERSION'
    import os
    print 'import os'
    import zipfile
    print 'import ZipFile'
    import sys
    print 'import sys'
    import urllib2
    print 'import urllib2'
    import time
    print 'all imports done (time last import)'
    raise

    print 'Before anything apart from importing'

    app = QApplication(sys.argv)
    update_dialog = QWidget()
    update_dialog.resize(350, 100)
    update_dialog.setWindowTitle('Updater')
    update_dialog.show()

    update_dialog_lbl = QLabel(update_dialog)
    update_dialog_lbl.setGeometry(10, 40, 340, 25)
    update_dialog_lbl.setOpenExternalLinks(True)
    update_dialog_lbl.setText('Updating! (Screen will hang, it\'s normal.)')

    # sys.exit(app.exec_())

    running = True
    versionNew = 0
    success = False

    updater()
    # this code will stall the rest of the code until the thread says 'running = False'
    # This means that the code past this will run only after the thread said
    # it could do that.
    while running:
        time.sleep(1)
    if success:
        update_dialog_lbl.setText('Updating has finished. ' +
                                  r'Find the patchnotes <a href="http://www.league-insanity.tk/?page_id=54">here</a>. v' + str(versionNew))
    else:
        update_dialog_lbl.setText(
            'Update was not successful, try running it again.')
