describe('Issue 247', () => {
    it('Int', () => {
      cy.visit('http://localhost:5000/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtqgFyoAUAlKoEmEqAkgHaGYC%2BmmhAFgKYgUGbLgLEStVAB5UARgAMAOk6YgA')
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')
      cy.get('p-dialog').find('app-undo').find('button').click()  // explain panel
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')
    }),
    it('Date', () => {
      // enter today's date
      cy.visit('http://localhost:4201/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtgDSoDOEJApqgFyoAUAlKoEmEqAIkbZgF9MmQgAtaIFBmy4CxEm1QBeADyoAxABUA8twCCATQB0MnHNKKlVGrTYmhQA')
      cy.get('app-symbol-value-selector').contains('datum').find('input').click()
      cy.contains('Today').click()
      cy.get('app-symbol-value-selector').contains('datum').find('input').invoke('val')
      .then(date_val =>
        cy.get('app-symbol-value-selector').contains('same').contains(date_val))

      // clear the date
      cy.get('app-symbol-value-selector').find('input').click()
      cy.get('button').contains('Clear').click()
      cy.get('app-symbol-value-selector').contains('same').should('not.include.text', '#')


      // reset the date
      cy.get('app-symbol-value-selector').contains('datum').find('input').click()
      cy.contains('Today').click()
      cy.contains('Reset').click()
      cy.contains('Full').click()
      cy.get('app-symbol-value-selector').contains('datum').find('input').should('have.value', '')
    })
  })