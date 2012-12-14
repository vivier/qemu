Installing the QEMU Guest Agent on Windows guests
--------------------------------------------------

The QEMU Guest Agent for Windows is contained in the single executable
file, qemu-ga.exe.  In addition to this executable, the guest agent
also relies on the following DLLs:

   libglib-2.0-0.dll
   iconv.dll
   libintl-8.dll

To install the guest agent:

1. Create a directory/folder on the Windows guest to contain the guest agent
   executable (e.g. c:\qemu-ga)

2. Copy the qemu-ga.exe, and any required DLL files, to the folder created in 
   step 1

3. To see all valid options for the guest agent, run 'qemu-ga.exe --help' from
   the folder where you copied the files in step 1.

4. Register the guest agent as a service by running it from the command line
   with the '--service install' option, along with other desired options.

   NOTE: In order to install or uninstall the guest agent as a service, you
         must have launched the cmd shell with admin privileges.  In order to
         do this under most versions of Windows, when launching 'cmd' from the
         start menu run box, press 'ctrl-shift-enter' instead of just 'enter'.

