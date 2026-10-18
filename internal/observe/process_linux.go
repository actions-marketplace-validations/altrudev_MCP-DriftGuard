//go:build linux

package observe

import (
 "os/exec"
 "syscall"
)

func configureStdioProcess(cmd *exec.Cmd) {
 cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid:true}
}

func terminateStdioProcess(cmd *exec.Cmd) {
 if cmd.Process != nil {
  // Entire launched process group, including descendants still in it.
  _ = syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
  _ = cmd.Process.Kill()
 }
}
