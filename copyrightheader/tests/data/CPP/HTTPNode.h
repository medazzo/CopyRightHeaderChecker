/**
 *  \copyright Copyright (c) 2011, 2012 All Right Reserved
 *  \brief implementation de Http Node Tree
 *  \file  HTTPNode.h
 *  \date 11 juin 2013
 *  \author Azzouni Mohamed
 */

#ifndef HTTPNODE_H_
#define HTTPNODE_H_

#include "Neptune.h"

#include "CMopServer.h"

namespace cmop {

/**
 * \class HTTPNode
 * \brief The handlers tree .
 */
class HTTPNode : public NPT_HttpRequestHandler {
 public:
  /**
   * \brief destructor of HTTPNode
   */
  ~HTTPNode();

  /**
   * \brief   instantiate a Http Node on Http Server Tree
   */
  HTTPNode();

  /**
   * \brief   instantiate a Http Node on Http Server Tree
   * \param   node :the content of the node type of IHTTP_Handler
   */
  HTTPNode(IHTTPHandler *node);

  /**
   * \brief   operator == used to compare
   * \param   other :the other Http Node
   * \return  true if segment on two node is equal else false.
   */
  bool operator==(const HTTPNode &other);

  /**
   * \brief   get the handler of the Node
   * \return  IHTTPHandler the handler of the node
   */
  IHTTPHandler* getHandler();

  /**
   * \brief   operator == used to compare
   * \param   other :the other Http Node
   * \return  true if segment on two node is equal else false.
   */
  bool operator==(const ::NPT_String &other);
  /**
   * \brief   StartsWith used to compare
   * \param   other :the other Http Node
   * \return  true if segment on two node is equal else false.
   */
  bool StartsWith(const NPT_String &other);

  /**
   * \brief   search segment on children nodes
   * \param   segment :searched segment
   * \param   found pointer on node , Update it with pointer if found
   * \return  True if segment is found and found id updated else False.
   */
  bool FindSegmentChildNode(::NPT_String segment, HTTPNode *&found);

  /**
   * \brief   get the node content pointer type of IHTTP_Handler
   * \return  pointer to the content of this node
   */
  IHTTPHandler* getNodeHandler();

  /**
   * \brief  used to set the Response : see  NPT_HttpRequestHandler::SetupResponse
   * \param   request : the client query
   * \param   context : the request http context.
   * \param   response : the response
   * \return  NPT_SUCCES else Neptune code error .
   */
  NPT_Result SetupResponse(::NPT_HttpRequest &request,
                           const ::NPT_HttpRequestContext &context,
                           ::NPT_HttpResponse &response);

 public:
  /** \brief   pointer to the content of the node type of IHTTP_Handler*/
  IHTTPHandler *m_node;
};
}
#endif /* HTTPNODE_H_ */
