//go:build !linux

package observe

import "os/exec"

func configureStdioProcess(cmd *exec.Cmd) {}
func terminateStdioProcess(cmd *exec.Cmd) {
 if cmd.Process != nil { _ = cmd.Process.Kill() }
}
