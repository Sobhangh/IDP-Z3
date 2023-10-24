describe('Issue 247', () => {
    it('Int', () => {
      cy.visit('http://localhost:5000/?FDBuHsGMEMCMFcA20BOBPABANQwb2AJAAuaADgKYYCy5RAFuACYD6RGAXALx4YBy0AS0QAaDAHFE8cqIDKkFOQDuGAL6FGAgGaaBkJCWbhNzGvSbtqtBizYBaAHwYAkgDsihSAwDO5F8wC2VuYYGA6WZjYe3r7MGtq6%2BmgWoY6u7gQAKkLSGKTJYQBC4OCIwGogXkQo8JBE8AoYMhY4%2BARxOnqIBkYmQYwc3LgAFPxCAJQpGACMokMSUhNhAAyzcgqKi44ATCoAdGXA9OTg6BgZzXggBAD010RwiOTMAGyEANr3sI8vALqEWY8hhNOI4AH5DTzgHx%2BQIRIEYbhrJQYAA%2BGEh0ICfXh3FGiDG%2B2AIRCGJisOsOPmlDRpJh2LGoM4VP2BA%2BDyeAA4-gRWgRabEtB1EjiMO0El00IZjKYKfzyUwgRMADy2DBVKQstTlYCkFBQciMeqUfyCFxA-C62gGXUCNxDfxMciIZjkAAepGgLkYQwywhkwhNrs4UzGYwOQA')

      // click Tile
      cy.assert_true('Tile');
      // method should be Glue
      cy.get('app-symbol-value-selector').contains('method').find('button').find('span').should('have.text', 'Glue')
    })
  })