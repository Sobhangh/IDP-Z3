describe('template spec', () => {
    it('passes', () => {
      cy.visit('http://localhost:4201/')
      cy.contains('File').click()
      cy.contains('Polygon').click()
      cy.get('.ui-panel-title').contains('sides')

      // assert not irregular
      cy.contains('app-symbol-value-selector', 'irregular').find('.ui-button-danger').click();
      // assert regular triangle
      cy.contains('app-symbol-value-selector', 'regular triangle').find('.ui-button-success').click();
      // retract not irregular
      cy.contains('app-symbol-value-selector', 'irregular').find('.ui-button-warning').not(':hidden').click();
      // retract regular triangle
      cy.get('app-symbol-value-selector').filter(':has(app-symbol-value-selector-buttons)').contains('regular triangle')
        .find('.ui-button-warning').not(':hidden').click();

      cy.get('app-symbol-value-selector').filter(':has(app-symbol-value-selector-buttons)').contains('regular triangle')
        .find('.ui-button-success')
    })
  })