from gi.repository import Nautilus, GObject, GLib, Notify
import logging
import os


class NauNapiExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        logging.basicConfig(filename='/tmp/test-log',
                            level=logging.DEBUG)

        self._log = logging.getLogger('naunapi')
        self._log.debug('starting up')
        self._notifications = True
        self._pynapi = 'pynapi'
        Notify.init('NauNapi')

    def _pynapi_finished(self, pid, status, stdout):
        """

        Arguments:
        - `stdout`: stdout of pynapi
        """
        self._log.debug('pynapi finished, status: %d', status)

        if status == 0:
            with os.fdopen(stdout) as infile:
                path = infile.read()
                message = 'Subtitles downloaded to %s' % (path)
                n = Notify.Notification.new('Info',
                                            message,
                                            'dialog-information')

                self._log.debug('subtitle path: %s', path)
        else:
                n = Notify.Notification.new('Error',
                                            'Subtitles not found',
                                            'dialog-information')

        n.show()


    def _activate_cb(self, menu, path):
        """
        """
        self._log.debug('acivate')
        napi_cmd = ['pynapi', '--tool-mode', path]
        self._log.debug('spawning command: %s', ' '.join(napi_cmd))

        (pid, _, stdout, _) = GLib.spawn_async(napi_cmd,
                                               standard_output=True,
                                               flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SPAWN_DO_NOT_REAP_CHILD)
        GLib.child_watch_add(pid, self._pynapi_finished, stdout,
                             GLib.PRIORITY_DEFAULT)

        self._log.debug('pynapi started as PID %d', pid)

    def get_file_items(self, window, files):
        self._log.debug('files')
        self._log.debug('%r', files)

        if len(files) != 1:
            return

        selected_file = files[0]
        path = selected_file.get_location().get_path()
        mime = selected_file.get_mime_type()

        self._log.debug('file %s, mime: %s',
                        path, mime)

        # check if it's a video file'
        if not mime.startswith('video/'):
            self._log.debug('not a video file')
            return

        # create menu item
        menuitem = Nautilus.MenuItem(name='ExampleMenuProvider::Foo',
                                     label='Pobierz _napisy',
                                     tip='Pobierz napisy',
                                     icon='')

        menuitem.connect('activate', self._activate_cb, path)


        return menuitem,
