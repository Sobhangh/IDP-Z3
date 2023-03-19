describe('Issue 247', () => {
    it('Int', () => {
      cy.visit('http://localhost:5000/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtqgFyoAUAlKoEmEqAkgHaGYC%2BmmhAFgKYgUGbLgLEStVAB5UARgAMAOk6YgA')
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')
      cy.get('p-dialog').find('app-undo').find('button').click()  // explain panel
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')
    }),
    it('Date', () => {
      cy.visit('http://localhost:4201/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtgDSoDOEJApqgFyoAUAlKoEmEqAIkbZgF9MmQgAtaIFBmy4CxEm1QAeVAGIAKgHluAQQCaAOhk45pRQF4qNWmyNCgA')
      cy.get('app-symbol-value-selector').contains('datum').find('input').type('#2023-01-01{enter}')
      cy.get('app-symbol-value-selector').contains('same').contains('#2023-01-01')
      cy.get('app-symbol-value-selector').find('input').click()
      cy.get('button').contains('Clear').click()
      cy.get('app-symbol-value-selector').contains('same').should('not.include.text', '#2023-01-01')


      cy.get('app-symbol-value-selector').contains('datum').find('input').type('#2023-01-01{enter}')
      cy.contains('Reset').click()
      cy.contains('Full').click()
      // TODO cy.get('app-symbol-value-selector').contains('datum').find('input').should('have.value', '')
    })
  })