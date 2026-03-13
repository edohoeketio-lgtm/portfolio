import { test, expect } from '@playwright/test';

test.describe('Portfolio Architecture & UX', () => {
  
  test('brutalist mode and project visibility', async ({ page }) => {
    await page.goto('/');
    
    // Check main layout renders
    await expect(page.locator('.brutalist-name')).toHaveText('maurice');
    
    // Check projects exist
    const projectItems = page.locator('.brutalist-item');
    await expect(projectItems).toHaveCount(5); // stream fm, greatwood, shp.it, spectral ghost, etc.
  });

  test('conversational contact form (happy path)', async ({ page }) => {
    // Intercept formsubmit to avoid actually hitting standard email
    await page.route('https://formsubmit.co/ajax/edohoeketio@gmail.com', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ success: "true", message: "Form submitted successfully" })
      });
    });

    await page.goto('/');
    
    // Open chat
    await page.click('#brutalist-contact-btn');
    await expect(page.locator('#chat-modal')).toHaveClass(/open/);

    // Initial question is asked
    await expect(page.locator('.chat-messages')).toContainText('what\'s your name?');
    
    // Type name
    const chatInput = page.locator('#chat-input');
    await chatInput.fill('John Doe');
    await chatInput.press('Enter');
    
    // Check company question
    await expect(page.locator('.chat-messages')).toContainText('nice to meet you, John Doe!');
    await chatInput.fill('Acme Corp');
    await chatInput.press('Enter');
    
    // Check project question
    await expect(page.locator('.chat-messages')).toContainText('what are you looking to build?');
    await chatInput.fill('A magical web experience');
    await chatInput.press('Enter');
    
    // Check email question
    await expect(page.locator('.chat-messages')).toContainText('drop your email');
    await chatInput.fill('john@acme.com');
    await chatInput.press('Enter');
    
    // Wait for submission success UI
    await expect(page.locator('.chat-messages')).toContainText('perfect — I\'ve got everything I need', { timeout: 10000 });
  });

  test('conversational contact form (error path)', async ({ page }) => {
    // Mock a 500 error
    await page.route('https://formsubmit.co/ajax/edohoeketio@gmail.com', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: "Server Error" })
      });
    });

    await page.goto('/');
    
    // Open chat
    await page.click('#brutalist-contact-btn');
    
    // Fast track through inputs
    const chatInput = page.locator('#chat-input');
    await chatInput.fill('Test'); await chatInput.press('Enter');
    await chatInput.fill('Test Inc'); await chatInput.press('Enter');
    await chatInput.fill('Test Project'); await chatInput.press('Enter');
    await chatInput.fill('test@test.com'); await chatInput.press('Enter');
    
    // Wait for the simulated error message
    await expect(page.locator('.chat-messages')).toContainText('ah, something went wrong on my end.', { timeout: 10000 });
    await expect(chatInput).toHaveAttribute('placeholder', 'Error ✕');
  });
});
