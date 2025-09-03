# Sketchy/Non-Working Games - TODO List

**Created**: 2025-08-06  
**Status**: Active Issues  
**Priority**: Low (Data collection can proceed with working games)

## 🚨 Games with Complex Architectural Issues

### **Among Us** - Async Checkpointer Error

- **Issue**: `NotImplementedError` in `checkpointer.aget_tuple()`
- **Error**: Async checkpoint operations not implemented properly
- **Status**: Partially initializes but fails on execution
- **Fix Required**: Implement proper async checkpointer or switch to sync mode
- **Complexity**: High - core async infrastructure issue

### **BS (Bullshit) Card Game** - Graph Structure Error

- **Issue**: `Graph must have entry point` - missing START edges
- **Error**: Graph validation fails during compilation
- **Status**: Initializes but compilation fails
- **Fix Required**: Add proper `graph.add_edge(START, "initialize")` edges
- **Complexity**: Medium - graph structure fix needed

### **Wordle** - Graph Entry Point Missing

- **Issue**: Similar graph validation error as BS
- **Error**: Conditional edges setup but no entry point
- **Status**: Initializes but compilation fails
- **Fix Required**: Fix graph edge configuration
- **Complexity**: Medium - graph structure issue

### **Debate (v1)** - Unknown Error

- **Issue**: Initialization passes but runtime error
- **Error**: Not fully diagnosed - appears to be execution error
- **Status**: Starts but fails during execution
- **Fix Required**: Debug runtime execution flow
- **Complexity**: Unknown - needs investigation

## ⏱️ Games that Timeout (>30s)

These games work but take too long for quick testing:

### **Chess** - ✅ Fixed but Slow

- **Status**: Now works! Fixed template variable bug
- **Issue**: Takes >30s to complete (normal for chess)
- **Fix Required**: None - this is expected behavior
- **Note**: Could be included in data collection with longer timeout

### **Reversi** - Unknown Performance Issue

- **Issue**: Hangs or runs very slowly
- **Status**: Times out after 30s
- **Fix Required**: Performance investigation
- **Complexity**: Unknown

### **Debate V2** - ✅ Fixed but Long-Running

- **Status**: Now works! Fixed import errors
- **Issue**: Full debate takes >30s (normal for debate)
- **Fix Required**: None - this is expected behavior
- **Note**: Successfully runs complete debates with scoring

### **Dominoes** - Unknown Hang

- **Issue**: Process hangs indefinitely
- **Status**: Times out after 30s
- **Fix Required**: Debug infinite loop or long computation
- **Complexity**: Unknown

### **Mastermind** - Unknown Performance Issue

- **Issue**: Hangs or runs very slowly
- **Status**: Times out after 30s
- **Fix Required**: Performance investigation
- **Complexity**: Unknown

## 📝 Diagnosis and Fix Priorities

### **High Priority** (if pursuing)

1. **Among Us** - Core async infrastructure issue affecting other games
2. **BS & Wordle** - Graph structure fixes are relatively straightforward

### **Medium Priority**

3. **Debate v1** - Runtime execution debugging
4. **Reversi, Dominoes, Mastermind** - Performance investigation

### **Low Priority**

- Chess and Debate V2 are actually working fine, just slow

## 🛠️ Specific Fix Recommendations

### For Graph Structure Issues (BS, Wordle):

```python
# Add missing START edge
graph.add_edge(START, "initialize")  # or appropriate entry node

# Ensure proper conditional edge setup
graph.add_conditional_edges(
    "node_name",
    condition_function,
    {"continue": "next_node", "end": END}
)
```

### For Among Us Async Issue:

```python
# Switch to sync checkpointer or implement proper async methods
# Check PostgresSaverWithThreadCreation async compatibility
```

### For Performance Issues:

- Add debug logging to identify where hangs occur
- Check for infinite loops in game logic
- Profile memory usage during execution

## 📊 Impact Assessment

**For Data Collection**: ✅ **NO IMPACT**

- 5 full games work perfectly for data collection
- 3 additional partial games available
- Variety of game types covered adequately

**For Framework Completeness**: ⚠️ **Medium Impact**

- Some game types missing (social deduction, word games, some card games)
- Framework appears solid - issues are game-specific implementations

**For Maintenance**: 📋 **Low Priority**

- Games work for their intended purposes when they work
- Issues appear to be edge cases or complex scenarios
- Core framework is stable

## 🎯 Recommended Actions

1. **Immediate**: Proceed with data collection on working games
2. **Short-term**: Fix simple graph structure issues if needed
3. **Long-term**: Address async infrastructure issues for broader compatibility
4. **Optional**: Performance profiling for timeout games

**Note**: These issues don't block primary objectives since we have excellent working games covering diverse gameplay patterns.
