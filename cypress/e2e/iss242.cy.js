describe('template spec', () => {
    it('passes', () => {
      cy.visit('http://localhost:4201/')
      cy.contains('File').click()
      cy.contains('Polygon').click()
      cy.get('.ui-panel-title').contains('sides') // wait for loading

      cy.assert_false('irregular');
      cy.assert_true('regular triangle');
      cy.retract('irregular');
      cy.retract('regular triangle');

    cy.is_unset('regular triangle');
    })
  })