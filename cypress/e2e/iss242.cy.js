describe('template spec', () => {
    it('passes', () => {
      cy.visit('http://localhost:5000/')
      cy.contains('File').click()
      cy.contains('Polygon').click()
      cy.get('.ui-panel-title').contains('sides')

      cy.get('app-symbol-value-selector').contains('irregular').find('.ui-button-danger').click()
      cy.get('app-symbol-value-selector').contains('regular triangle').find('.ui-button-success').click()
      cy.get('app-symbol-value-selector').contains('irregular').find('.ui-button-warning').not(':hidden').click()
      cy.get('app-symbol-value-selector').contains('regular triangle').find('.ui-button-warning').not(':hidden').click()

      cy.get('app-symbol-value-selector').contains('regular triangle').find('.ui-button-success')
    })
  })