# Claude Code Notes & Tips

## Background Process Management

### Known Claude Code Timeout Issues

- **CLI timeout bug**: Default 1000ms timeout causes premature termination
- **WSL-specific timeouts**: Session timeouts in WSL environments
- **Hardcoded limits**: 2-minute command timeouts with no configuration
- **GitHub Issues**: #2489, #821, #424, #743

### Background Process Solutions

#### Basic nohup Pattern

```bash
nohup long_command > output_$(date +%Y%m%d_%H%M%S).log 2>&1 &
echo $!  # Get process ID
```

#### Advanced Python Process Management

```bash
# For Python processes that need signal handling
setsid nohup python script.py > output.log 2>&1 &
```

#### tmux (Recommended for Development)

```bash
tmux new-session -d -s haive_build
tmux send-keys -t haive_build "poetry run pytest" C-m
tmux attach -t haive_build  # To monitor
```

### Best Practices

- Always use nohup for tasks > 30 seconds
- Monitor with `ps aux | grep process_name`
- Use tmux for interactive development sessions
- Handle Python signal issues when needed

### When to Use Background Processes

- Long builds (> 1 minute)
- Test suites that run for extended periods
- File processing tasks
- Model training or heavy computations

### Don't Use For

- Quick commands (< 30 seconds)
- Commands needing interactive input
- Commands where immediate error feedback is critical
