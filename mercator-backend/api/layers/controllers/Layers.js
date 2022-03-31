'use strict';

/**
 * Layers.js controller
 *
 * @description: A set of functions called "actions" for managing `Layers`.
 */

module.exports = {

  /**
   * Retrieve layers records.
   *
   * @return {Object|Array}
   */

  find: async (ctx, next, { populate } = {}) => {
    if (ctx.query._q) {
      return strapi.services.layers.search(ctx.query);
    } else {
      return strapi.services.layers.fetchAll(ctx.query, populate);
    }
  },

  /**
   * Retrieve a layers record.
   *
   * @return {Object}
   */

  findOne: async (ctx) => {
    return strapi.services.layers.fetch(ctx.params);
  },

  /**
   * Count layers records.
   *
   * @return {Number}
   */

  count: async (ctx, next, { populate } = {}) => {
    return strapi.services.layers.count(ctx.query, populate);
  },

  /**
   * Create a/an layers record.
   *
   * @return {Object}
   */

  create: async (ctx) => {
    return strapi.services.layers.add(ctx.request.body);
  },

  /**
   * Update a/an layers record.
   *
   * @return {Object}
   */

  update: async (ctx, next) => {
    return strapi.services.layers.edit(ctx.params, ctx.request.body) ;
  },

  /**
   * Destroy a/an layers record.
   *
   * @return {Object}
   */

  destroy: async (ctx, next) => {
    return strapi.services.layers.remove(ctx.params);
  }
};
