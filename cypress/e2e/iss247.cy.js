describe('Issue 247', () => {
    it('passes', () => {
      cy.visit('http://localhost:5000/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtqgFyoAUAlKoEmEqAkgHaGYC%2BmmhAFgKYgUGbLgLEStVAB5UARgAMAOk6YgA')
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')
      cy.get('p-dialog').find('app-undo')  // explain panel
    })
  })