import { test, expect } from '@playwright/test'

const BASE_URL = process.env.BASE_URL || 'https://qualifica.loft.com.br'

test.describe('Cadastro - Dados Pessoais', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/cadastro`)
  })

  test.describe('FUNC - Functionality', () => {
    test('FUNC-001: Cadastro com dados válidos', async ({ page }) => {
      // Arrange
      const testEmail = `teste+${Date.now()}@example.com`

      // Act
      await page.getByLabel('Nome').fill('João')
      await page.getByLabel('Sobrenome').fill('Silva')
      await page.getByLabel('E-mail').fill(testEmail)
      await page.getByRole('button', { name: 'Criar conta' }).click()

      // Assert
      await expect(page.getByText('Verifique seu e-mail')).toBeVisible()
      await expect(page.getByText(testEmail)).toBeVisible()
    })

    test('FUNC-002: Validação de e-mail inválido', async ({ page }) => {
      // Act
      await page.getByLabel('E-mail').fill('email-invalido')
      await page.getByLabel('E-mail').blur()

      // Assert
      await expect(page.getByText(/e-mail.*inválido|formato.*incorreto/i)).toBeVisible()
    })

    test('FUNC-003: Validação de nome curto', async ({ page }) => {
      // Act
      await page.getByLabel('Nome').fill('J')
      await page.getByLabel('Nome').blur()

      // Assert
      await expect(page.getByText(/mínimo.*2.*caracteres/i)).toBeVisible()
    })

    test('FUNC-004: Campos obrigatórios vazios', async ({ page }) => {
      // Act
      await page.getByRole('button', { name: 'Criar conta' }).click()

      // Assert
      await expect(page.getByLabel('Nome')).toHaveAttribute('aria-invalid', 'true')
      await expect(page.getByLabel('Sobrenome')).toHaveAttribute('aria-invalid', 'true')
      await expect(page.getByLabel('E-mail')).toHaveAttribute('aria-invalid', 'true')
    })

    test('FUNC-005: Reenviar e-mail com cooldown', async ({ page }) => {
      // Arrange - complete signup first
      await page.getByLabel('Nome').fill('João')
      await page.getByLabel('Sobrenome').fill('Silva')
      await page.getByLabel('E-mail').fill(`teste+${Date.now()}@example.com`)
      await page.getByRole('button', { name: 'Criar conta' }).click()
      await expect(page.getByText('Verifique seu e-mail')).toBeVisible()

      // Act
      await page.getByRole('link', { name: /reenviar/i }).click()

      // Assert
      await expect(page.getByText(/60|segundos|aguarde/i)).toBeVisible()
      await expect(page.getByRole('link', { name: /reenviar/i })).toBeDisabled()
    })

    test('FUNC-006: Usar outro e-mail', async ({ page }) => {
      // Arrange - complete signup first
      await page.getByLabel('Nome').fill('João')
      await page.getByLabel('Sobrenome').fill('Silva')
      await page.getByLabel('E-mail').fill(`teste+${Date.now()}@example.com`)
      await page.getByRole('button', { name: 'Criar conta' }).click()
      await expect(page.getByText('Verifique seu e-mail')).toBeVisible()

      // Act
      await page.getByRole('link', { name: /usar outro e-mail/i }).click()

      // Assert
      await expect(page.getByLabel('Nome')).toBeVisible()
      await expect(page.getByLabel('E-mail')).toBeVisible()
    })

    test('FUNC-008: Magic link expirado', async ({ page }) => {
      // Arrange - simulate expired token
      const expiredToken = 'expired-test-token-123'

      // Act
      await page.goto(`${BASE_URL}/auth/verify?token=${expiredToken}`)

      // Assert
      await expect(page.getByText(/link.*expirado/i)).toBeVisible()
      await expect(page.getByRole('link', { name: /solicitar.*novo/i })).toBeVisible()
    })

    test('FUNC-009: Magic link inválido', async ({ page }) => {
      // Arrange - invalid token
      const invalidToken = 'invalid-token-xyz'

      // Act
      await page.goto(`${BASE_URL}/auth/verify?token=${invalidToken}`)

      // Assert
      await expect(page.getByText(/link.*inválido/i)).toBeVisible()
    })
  })

  test.describe('SEC - Security', () => {
    test('SEC-001: Brute force protection', async ({ page }) => {
      // Act - attempt 6 signups rapidly
      for (let i = 0; i < 6; i++) {
        await page.goto(`${BASE_URL}/cadastro`)
        await page.getByLabel('Nome').fill('Test')
        await page.getByLabel('Sobrenome').fill('User')
        await page.getByLabel('E-mail').fill(`brute+${i}@test.com`)
        await page.getByRole('button', { name: 'Criar conta' }).click()

        if (i >= 5) {
          // Assert - should be blocked
          await expect(page.getByText(/bloqueado|muitas tentativas|aguarde/i)).toBeVisible()
        }
      }
    })

    test('SEC-003: XSS no formulário', async ({ page }) => {
      // Arrange
      const xssPayload = '<script>alert(1)</script>'

      // Act
      await page.getByLabel('Nome').fill(xssPayload)
      await page.getByLabel('Sobrenome').fill(xssPayload)
      await page.getByLabel('E-mail').fill('test@example.com')

      // Assert - script should not execute, check escaped content
      const nameValue = await page.getByLabel('Nome').inputValue()
      expect(nameValue).toBe(xssPayload) // Value preserved but escaped in DOM

      // Verify no alert dialog appeared
      let alertTriggered = false
      page.on('dialog', () => {
        alertTriggered = true
      })
      await page.waitForTimeout(500)
      expect(alertTriggered).toBe(false)
    })

    test('SEC-004: Token manipulation', async ({ page }) => {
      // Arrange - tampered token
      const tamperedToken = 'valid-token-modified-by-attacker'

      // Act
      await page.goto(`${BASE_URL}/auth/verify?token=${tamperedToken}`)

      // Assert
      await expect(page.getByText(/link.*inválido/i)).toBeVisible()
    })

    test('SEC-006: HTTPS redirect', async ({ page }) => {
      // Act
      await page.goto(`http://qualifica.loft.com.br/cadastro`, {
        waitUntil: 'domcontentloaded',
      })

      // Assert
      expect(page.url()).toMatch(/^https:\/\//)
    })
  })

  test.describe('USAB - Usability', () => {
    test('USAB-001: Labels claros', async ({ page }) => {
      // Assert
      await expect(page.getByLabel('Nome')).toBeVisible()
      await expect(page.getByLabel('Sobrenome')).toBeVisible()
      await expect(page.getByLabel('E-mail')).toBeVisible()
    })

    test('USAB-003: Loading state', async ({ page }) => {
      // Arrange
      await page.getByLabel('Nome').fill('João')
      await page.getByLabel('Sobrenome').fill('Silva')
      await page.getByLabel('E-mail').fill(`teste+${Date.now()}@example.com`)

      // Act
      await page.getByRole('button', { name: 'Criar conta' }).click()

      // Assert - should show loading indicator
      await expect(page.getByRole('button', { name: 'Criar conta' })).toBeDisabled()
      // Or check for loading spinner
      await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible()
    })
  })

  test.describe('RESP - Responsive', () => {
    test('RESP-001: Mobile (375px)', async ({ page }) => {
      // Arrange
      await page.setViewportSize({ width: 375, height: 667 })

      // Assert
      await expect(page.getByRole('button', { name: 'Criar conta' })).toBeVisible()
      await expect(page.getByLabel('Nome')).toBeVisible()

      // Check no horizontal scroll
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth)
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth)
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth)
    })

    test('RESP-004: Touch targets', async ({ page }) => {
      // Arrange
      await page.setViewportSize({ width: 375, height: 667 })

      // Act
      const button = page.getByRole('button', { name: 'Criar conta' })
      const boundingBox = await button.boundingBox()

      // Assert - minimum 44x44px
      expect(boundingBox?.height).toBeGreaterThanOrEqual(44)
      expect(boundingBox?.width).toBeGreaterThanOrEqual(44)
    })
  })

  test.describe('PERF - Performance', () => {
    test('PERF-001: Page load < 2s', async ({ page }) => {
      // Arrange
      const startTime = Date.now()

      // Act
      await page.goto(`${BASE_URL}/cadastro`, { waitUntil: 'domcontentloaded' })

      // Assert
      const loadTime = Date.now() - startTime
      expect(loadTime).toBeLessThan(2000)
    })
  })

  test.describe('A11Y - Accessibility', () => {
    test('A11Y-001: Navegação por teclado', async ({ page }) => {
      // Act - Tab through form
      await page.keyboard.press('Tab')
      await expect(page.getByLabel('Nome')).toBeFocused()

      await page.keyboard.press('Tab')
      await expect(page.getByLabel('Sobrenome')).toBeFocused()

      await page.keyboard.press('Tab')
      await expect(page.getByLabel('E-mail')).toBeFocused()

      await page.keyboard.press('Tab')
      await expect(page.getByRole('button', { name: 'Criar conta' })).toBeFocused()
    })

    test('A11Y-002: Focus indicator', async ({ page }) => {
      // Act
      await page.getByLabel('Nome').focus()

      // Assert - check focus is visible (outline or ring)
      const focusStyles = await page.getByLabel('Nome').evaluate((el) => {
        const styles = getComputedStyle(el)
        return {
          outline: styles.outline,
          boxShadow: styles.boxShadow,
        }
      })

      // Should have some visible focus indicator
      expect(focusStyles.outline !== 'none' || focusStyles.boxShadow !== 'none').toBe(true)
    })

    test('A11Y-003: Labels de formulário', async ({ page }) => {
      // Assert - all inputs have associated labels
      const nameInput = page.getByLabel('Nome')
      const sobrenomeInput = page.getByLabel('Sobrenome')
      const emailInput = page.getByLabel('E-mail')

      await expect(nameInput).toBeVisible()
      await expect(sobrenomeInput).toBeVisible()
      await expect(emailInput).toBeVisible()

      // Verify aria-labelledby or label association
      const nameId = await nameInput.getAttribute('id')
      const label = page.locator(`label[for="${nameId}"]`)
      await expect(label).toBeVisible()
    })
  })
})
