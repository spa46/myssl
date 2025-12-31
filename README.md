# myssl

# Test Methods 
1. s_client
2. verify

## Detailed Comparison

| Test Item | Method 1 (s_client) | Method 2 (verify) | Better Method |
|------------|------------------|----------------|-------------|
| **Valid Certificate** | Possible | Possible | Same |
| **Revoked Certificate** | Difficult | Easy | **Method 2** |
| **Expired Certificate** | Difficult | Easy | **Method 2** |
| **Bad CA** | Possible | Possible | Same |
| **Certificate Chain** | Possible | Possible | Same |
| **TLS Handshake** | Possible | Not Possible | **Method 1** |
| **Cipher Suite** | Possible | Not Possible | **Method 1** |
| **Automation** | Complex | Simple | **Method 2** |
| **Execution Speed** | Slow | Fast | **Method 2** |

## Recommended Methods by Purpose

| Purpose | Recommended Method | Reason |
|------|----------|------|
| **Certificate Validation** | **Method 2** | More test cases, easier, faster |
| **TLS Handshake** | Method 1 | Actual connection testing |
| **CI/CD Automation** | **Method 2** | Stable, fewer dependencies |
| **Production Verification** | Method 1 | Reflects real environment |
