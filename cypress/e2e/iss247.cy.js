describe('Issue 247', () => {
    it('Int', () => {
      cy.visit('http://localhost:4201/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtqgFyoAUAlKoEmEqAkgHaGYC%2BmmhAFgKYgUGbLgLEStVAB5UARgAMAOk6YgA')
      // enter incorrect 15
      cy.get('app-symbol-value-selector').find('input').type('15{enter}')

      // explain panel shows error; reset it
      cy.get('p-dialog').find('app-undo').contains('datum() = 15')
      cy.get('p-dialog').find('app-undo').find('button').click()
      cy.get('app-symbol-value-selector').find('input').should('have.value', '')
    }),
    it('Date', () => {
      // enter today's date
      cy.visit('http://localhost:4201/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtgDSoDOEJApqgFyoAUAlKoEmEqAIkbZgF9MmQgAtaIFBmy4CxEm1QBeADyoAxABUA8twCCATQB0MnHNKKlVGrTYmhQA')
      cy.get('app-symbol-value-selector').contains('datum').find('input').click()
      cy.contains('Today').click()

      // same value in 'same'
      cy.get('app-symbol-value-selector').contains('datum').find('input').invoke('val')
      .then(date_val =>
        cy.get('app-symbol-value-selector').contains('same').contains(date_val))

      // clear the date
      cy.get('app-symbol-value-selector').find('input').click()
      cy.get('button').contains('Clear').click()
      cy.get('app-symbol-value-selector').contains('same').should('have.value', '')


      // enter and reset the date
      cy.get('app-symbol-value-selector').contains('datum').find('input').click()
      cy.contains('Today').click()
      cy.contains('Reset').click()
      cy.contains('Full').click()
      cy.get('app-symbol-value-selector').contains('datum').find('input').should('have.value', '')
    }),
    it('Date2', () => {
      // enter today's date
      cy.visit('http://localhost:4201/?G4ewxghgRgrgNhATgTwAQG8BQqeoCYQAuMAtgDSoDOEJAphQcSQEyoBcqAFAJSqBJhKgAiRWpgC%2BmTIQAWtECgzZcjUj1QBeADyoAxABUA8oICCATQB0SnCpJr1VGrR6Xc%2BIqWZrt%2Bo2csSgA')
      cy.get('app-symbol-value-selector').contains('datum2').find('input').click()
      cy.contains('Today').click()
      // explain panel shows error
      cy.get('p-dialog').find('app-undo').contains('datum2() = #')
    })
  })